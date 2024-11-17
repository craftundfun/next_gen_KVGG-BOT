from discord import Client


class CommandWorker:

    def __init__(self, client: Client):
        self.client = client

    async def prepareCommand(self, **kwargs):
        print("before command")

    async def afterCommand(self):
        print("after command")
