from discord import Client

from src.Logging.Logger import Logger

logger = Logger("CommandWorker")


class CommandWorker:

    def __init__(self, client: Client):
        self.client = client

    async def prepareCommand(self, **kwargs):
        logger.debug("before command")

    async def afterCommand(self):
        logger.debug("after command")
