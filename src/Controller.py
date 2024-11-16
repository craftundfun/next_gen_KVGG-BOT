from os import environ

from discord import Intents

from src.Client import Client
from src.command.CommandManager import CommandManager
from src.command.PingCommand import PingCommand


class Controller:

    def __init__(self):
        self.token = environ.get("DISCORD_TOKEN")

        if not self.token:
            print("No token provided")
            exit(1)

        self.client = Client(self, intents=Intents.all())
        self.commandManager = CommandManager(self.client)
        self.commandManager.add_command(PingCommand)

    def run(self):
        try:
            self.client.run(self.token, reconnect=True)
        except Exception as error:
            print(f"Error: {error}")
            exit(1)

    async def botReady(self):
        await self.commandManager.syncCommands()
        print("Bot is ready")

        # await self.commandManager.removeCommands()
