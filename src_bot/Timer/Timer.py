import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src_bot.Client.Client import Client
from src_bot.Interface.Client.ClientReadyListenerInterface import ClientReadyListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("Timer")


class Timer(ClientReadyListenerInterface):

    def __init__(self, client: Client):
        self.scheduler = AsyncIOScheduler()
        self.client = client

        self.registerListeners()

    def registerListeners(self):
        """
        Register the listeners for the timer
        """
        self.client.addListener(self.onBotReady, ClientListenerType.READY)
        logger.debug("Registered listeners")

    async def onBotReady(self):
        """
        Start the timer
        """
        try:
            logger.debug("Starting timer")
            self.scheduler.start()
            logger.info("Timer started")
        except Exception as error:
            logger.error("Failed to start timer", exc_info=error)

            sys.exit(1)

    def addJob(
            self,
            job: callable,
            timeToRun: datetime,
            identifier: str,
            **kwargs,
    ):
        """
        Add a job to the scheduler to run at the given time

        :param job: Job to run
        :param timeToRun: Time to run the job
        :param identifier: Identifier of the job
        :param kwargs: Additional arguments for the job
        """
        # otherwise the IDE will complain about the type of the misfire_grace_time
        # noinspection PyTypeChecker
        self.scheduler.add_job(
            job,
            "date",
            run_date=timeToRun,
            id=identifier,
            # run the job regardless of how late it is
            # maybe change that in the future
            misfire_grace_time=None,
            kwargs=kwargs,
        )

        logger.debug(f"Added job ({identifier}) to scheduler")

    async def removeJob(self, identifier: str) -> bool:
        """
        Remove a job from the scheduler with the given identifier

        :param identifier: Identifier of the job
        :return: True if the job was removed successfully, False otherwise
        """
        try:
            self.scheduler.remove_job(identifier)
        except Exception as error:
            logger.error(f"Failed to remove job ({identifier}) from scheduler", exc_info=error)

            return False
        else:
            logger.debug(f"Removed job ({identifier}) from scheduler")

            return True
