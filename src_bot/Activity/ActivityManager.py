from asyncio import Lock

from discord import Member, CustomActivity, Streaming, BaseActivity
from sqlalchemy import select, null, insert
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime, timezone, timedelta

from database.Domain.models.Activity import Activity
from database.Domain.models.ActivityHistory import ActivityHistory
from database.Domain.models.ActivityMapping import ActivityMapping
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Logging.Logger import Logger
from src_bot.Types.ActivityManagerType import ActivityManagerType
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("ActivityManager")


class ActivityManager:
    _self = None

    activityStartListener = []
    activitySwitchListener = []
    activityStopListener = []

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()
        self.lock = Lock()

        self.registerListeners()

    # Singleton pattern to ensure the lock is shared between all instances
    def __new__(cls, *args, **kwargs) -> "ActivityManager":
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def addListener(self, listener: callable, listenerType: ActivityManagerType):
        """
        Add a listener to the ActivityManager.

        :param listener: The listener to add.
        :param listenerType: The type of the listener.
        """
        match listenerType:
            case ActivityManagerType.ACTIVITY_START:
                self.activityStartListener.append(listener)
            case ActivityManagerType.ACTIVITY_SWITCH:
                self.activitySwitchListener.append(listener)
            case ActivityManagerType.ACTIVITY_STOP:
                self.activityStopListener.append(listener)
            case _:
                logger.error(f"Unknown listener type: {listenerType}")

    def registerListeners(self):
        """
        Register all listeners for the ActivityManager.
        """
        self.client.addListener(self.onActivityUpdate, ClientListenerType.ACTIVITY_UPDATE)
        logger.debug("Registered ActivityManager listener")

    # noinspection PyMethodMayBeStatic
    def _isActivityFeasible(self, activity: BaseActivity) -> bool:
        """
        Check if the activity is feasible for the activity manager.

        :param activity: The activity to check.
        :return: True if the activity is feasible, otherwise False.
        """
        return not isinstance(activity, CustomActivity) and not isinstance(activity, Streaming)

    # noinspection PyMethodMayBeStatic
    def _getSelectQueryForActivity(self, activity: BaseActivity) -> tuple[select, bool]:
        """
        Get the select query for the activity based on the application ID or the activity name.

        :param activity: The activity to get the select query for.
        :return: The select query for the activity and a bool that's true if the activity has an application ID,
                 otherwise False.
        """
        try:
            # noinspection PyUnresolvedReferences
            return select(Activity).where(Activity.external_activity_id == activity.application_id), True
        except AttributeError:
            # we don't care about a levenstein distance, we can simply use the activity mapping
            # noinspection PyUnresolvedReferences
            return select(Activity).where(Activity.name == activity.name), False

    # noinspection PyMethodMayBeStatic
    def _getActivityHistoryInsertQuery(self, member: Member, activity: Activity, eventId: int,
                                       endtime: datetime) -> insert:
        """
        Get the insert query for the activity history.

        :param member: The member to get the insert query for.
        :param activity: The activity to get the insert query for.
        :param eventId: The event ID for the activity history.
        :return: The insert query for the activity history
        """
        return insert(ActivityHistory).values(
            discord_id=member.id,
            guild_id=member.guild.id,
            # fetch the correct primary activity ID from the mapping table
            primary_activity_id=(
                select(ActivityMapping.primary_activity_id)
                .where(ActivityMapping.secondary_activity_id == activity.id)
                .scalar_subquery()
            ),
            event_id=eventId,
            # even though the time is set in the database, we set it here to avoid any issues with the order of the
            # events
            time=endtime,
        )

    def _getActivity(self, selectQuery: select, activity: BaseActivity, hasApplicationId: bool) -> Activity | None:
        """
        Get the activity from the database or insert it if it does not exist.

        :param selectQuery: The select query for the activity.
        :param activity: The activity to insert if it does not exist.
        :param hasApplicationId: True if the activity has an application ID, otherwise False.
        :return: The activity. None if an error occurred.
        """
        try:
            return self.session.execute(selectQuery).scalars().one()
        except NoResultFound:
            logger.debug(f"New activity found: {activity}")

            # noinspection PyUnresolvedReferences
            activity = Activity(
                name=activity.name,
                external_activity_id=activity.application_id if hasApplicationId else null(),
            )

            self.session.add(activity)
            # commit here to trigger the database trigger
            self.session.commit()
        except Exception as error:
            logger.error("Error while getting activity from database", exc_info=error)

            return None

    async def onActivityUpdate(self, before: Member, after: Member):
        """
        Handle the activity update event.

        :param before: The member before the activity update.
        :param after: The member after the activity update.
        """
        # 1: started an activity, 2: switched an activity, 3: stopped an activity
        case = -1
        # track when the activity was stopped to avoid getting more time within the database actions
        # create an aware datetime object to calculate the time later
        # TODO revert
        endtime = datetime.now(timezone.utc)

        async with self.lock:
            # open database session only after acquiring the lock
            with self.session:
                # member started an activity
                if not before.activity and after.activity:
                    logger.debug(f"{after.display_name, after.id} started the activity {after.activity} "
                                 f"on {after.guild.name, after.guild.id}")

                    if not self._isActivityFeasible(after.activity):
                        logger.debug(f"{after.display_name, after.id} started an activity that is not feasible for the "
                                     "tracking")

                        return

                    # use a boolean for the application id, otherwise every access would end in an AttributeError
                    selectQuery, hasApplicationId = self._getSelectQueryForActivity(after.activity)
                    activity = self._getActivity(selectQuery, after.activity, hasApplicationId)

                    if not activity:
                        return

                    insertQuery = self._getActivityHistoryInsertQuery(after, activity, 10, endtime)

                    try:
                        self.session.execute(insertQuery)
                        self.session.commit()
                    except Exception as error:
                        logger.error(
                            f"Error while inserting activity history into database. Insert-Query: {insertQuery}",
                            exc_info=error, )

                        self.session.rollback()
                    else:
                        logger.debug(f"Inserted activity history for {after.display_name, after.id} "
                                     f"on {after.guild.name, after.guild.id}")

                    case = 1

                # member switched activity
                elif before.activity and after.activity:
                    logger.debug(f"{after.display_name, after.id} switched the activity from {before.activity} to "
                                 f"{after.activity} on {after.guild.name, after.guild.id}")

                    if not self._isActivityFeasible(before.activity) or not self._isActivityFeasible(after.activity):
                        logger.debug(
                            f"{after.display_name, after.id} switched to an activity that is not feasible for the "
                            "tracking")

                        return

                    selectQueryBefore, hasApplicationIdBefore = self._getSelectQueryForActivity(before.activity)
                    selectQueryAfter, hasApplicationIdAfter = self._getSelectQueryForActivity(after.activity)

                    # sometimes an activity just switches details etc., so we need to check if the activity is the same
                    if hasApplicationIdBefore and hasApplicationIdAfter:
                        if before.activity.application_id == after.activity.application_id:
                            return
                    else:
                        if before.activity.name == after.activity.name:
                            return

                    activityBefore = self._getActivity(selectQueryBefore, before.activity, hasApplicationIdBefore)
                    activityAfter = self._getActivity(selectQueryAfter, after.activity, hasApplicationIdAfter)

                    if not activityBefore or not activityAfter:
                        return

                    insertQueryBefore = self._getActivityHistoryInsertQuery(before, activityBefore, 11, endtime)
                    insertQueryAfter = self._getActivityHistoryInsertQuery(after, activityAfter, 10, endtime)

                    try:
                        self.session.execute(insertQueryBefore)
                        self.session.execute(insertQueryAfter)
                        self.session.commit()
                    except Exception as error:
                        logger.error(
                            f"Error while inserting activity history into database. Insert-Query: "
                            f"{insertQueryBefore} and {insertQueryAfter}",
                            exc_info=error,
                        )

                        self.session.rollback()
                    else:
                        logger.debug(f"Inserted activity history for {after.display_name, after.id} "
                                     f"on {after.guild.name, after.guild.id}")

                    case = 2
                    activityId = activityBefore.id

                # member stopped an activity
                elif before.activity and not after.activity:
                    logger.debug(f"{before.display_name, before.id} stopped the activity {before.activity} "
                                 f"on {before.guild.name, before.guild.id}")

                    if not self._isActivityFeasible(before.activity):
                        logger.debug(
                            f"{before.display_name, before.id} stopped an activity that is not feasible for the "
                            "tracking")

                        return

                    selectQuery, hasApplicationId = self._getSelectQueryForActivity(before.activity)
                    activity = self._getActivity(selectQuery, before.activity, hasApplicationId)

                    if not activity:
                        return

                    insertQuery = self._getActivityHistoryInsertQuery(after, activity, 11, endtime)

                    # TODO maybe do this in a function as well
                    try:
                        self.session.execute(insertQuery)
                        self.session.commit()
                    except Exception as error:
                        logger.error(
                            f"Error while inserting activity history into database. Insert-Query: {insertQuery}",
                            exc_info=error, )

                        self.session.rollback()
                    else:
                        logger.debug(f"Inserted activity history for {after.display_name, after.id} "
                                     f"on {after.guild.name, after.guild.id}")

                    case = 3
                    activityId = activity.id

        match case:
            case 1:
                logger.debug("Notifying activity start listeners")

                for listener in self.activityStartListener:
                    await listener(after)
            case 2:
                logger.debug("Notifying activity switch listeners")

                for listener in self.activitySwitchListener:
                    await listener(before, after)

                # also notify the stop listeners, as the activity is stopped before another one is started
                for listener in self.activityStopListener:
                    # we need to pass the activity ID of the activity that was stopped, otherwise we would have
                    # enormous overhead to fetch it again
                    await listener(before, endtime, activityId)
            case 3:
                logger.debug("Notifying activity end listeners")

                for listener in self.activityStopListener:
                    await listener(before, endtime, activityId)
            case _:
                logger.error(f"Unknown case: {case}")
