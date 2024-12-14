from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src_bot.Client.Client import Client
from src_bot.Logging.Logger import Logger

logger = Logger("Timer")


class Timer:

    def __init__(self, client: Client):
        self.scheduler = AsyncIOScheduler()
        self.client = client

        self.scheduler.start()

    async def addJob(self,
                     job: callable,
                     timeToRun: datetime,
                     identifier: str,
                     **kwargs):
        self.scheduler.add_job(
            job,
            "date",
            run_date=timeToRun,
            id=identifier,
            kwargs=kwargs,
        )
