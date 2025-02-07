from discord import Member, CustomActivity, Streaming, BaseActivity
from sqlalchemy import select, null, insert
from sqlalchemy.orm.exc import NoResultFound

from database.Domain.models.Activity import Activity
from database.Domain.models.ActivityHistory import ActivityHistory
from database.Domain.models.ActivityMapping import ActivityMapping
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("ActivityManager")


class ActivityManager:

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()

        self.registerListeners()

    def registerListeners(self):
        """
        Register all listeners for the ActivityManager.
        """
        self.client.addListener(self.onActivityUpdate, ClientListenerType.ACTIVITY_UPDATE)
        logger.debug("Registered ActivityManager listener")

    def _isActivityFeasible(self, activity: BaseActivity) -> bool:
        """
        Check if the activity is feasible for the activity manager.

        :param activity: The activity to check.
        :return: True if the activity is feasible, otherwise False.
        """
        return not isinstance(activity, CustomActivity) and not isinstance(activity, Streaming)

    # def _getSelectQueryForActivity(self, activity: BaseActivity):

    async def onActivityUpdate(self, before: Member, after: Member):
        """
        Handle the activity update event.

        :param before: The member before the activity update.
        :param after: The member after the activity update.
        """
        with self.session:
            # member started an activity
            if not before.activity and after.activity:
                logger.debug(f"{after.display_name, after.id} started the activity {after.activity} "
                             f"on {after.guild.name, after.guild.id}")

                if not self._isActivityFeasible(after.activity):
                    logger.debug(f"{after.display_name, after.id} started an activity that is not feasible for the "
                                 "tracking")

                    return

                # use a boolean, otherwise every access would end in an AttributeError
                hasApplicationId = True

                # try to use the application ID
                try:
                    selectQuery = select(Activity).where(Activity.external_activity_id == after.activity.application_id)
                except AttributeError:
                    # we don't care about a levenstein distance, we can simply use the activity mapping
                    selectQuery = select(Activity).where(Activity.name == after.activity.name)
                    hasApplicationId = False

                try:
                    activity = self.session.execute(selectQuery).scalars().one()
                except NoResultFound:
                    logger.debug(f"New activity found: {after.activity}")

                    activity = Activity(
                        name=after.activity.name,
                        external_activity_id=after.activity.application_id if hasApplicationId else null(),
                    )

                    self.session.add(activity)
                    # commit here to trigger the database trigger
                    self.session.commit()
                except Exception as error:
                    logger.error("Error while getting activity from database", exc_info=error)

                    return

                insertQuery = insert(ActivityHistory).values(
                    discord_id=after.id,
                    guild_id=after.guild.id,
                    # fetch the correct primary activity ID from the mapping table
                    primary_activity_id=(
                        select(ActivityMapping.primary_activity_id)
                        .where(ActivityMapping.secondary_activity_id == activity.id)
                        .scalar_subquery()
                    ),
                    event_id=10,
                )

                try:
                    self.session.execute(insertQuery)
                    self.session.commit()
                except Exception as error:
                    logger.error(f"Error while inserting activity history into database. Insert-Query: {insertQuery}",
                                 exc_info=error, )

                    self.session.rollback()
                else:
                    logger.debug(f"Inserted activity history for {after.display_name, after.id} "
                                 f"on {after.guild.name, after.guild.id}")
            # member switched activity
            elif before.activity and after.activity:
                logger.debug(f"{after.display_name, after.id} switched the activity from {before.activity} to "
                             f"{after.activity} on {after.guild.name, after.guild.id}")

                if not self._isActivityFeasible(before.activity) or not self._isActivityFeasible(after.activity):
                    logger.debug(f"{after.display_name, after.id} switched to an activity that is not feasible for the "
                                 "tracking")

                    return


