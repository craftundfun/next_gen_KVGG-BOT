from os import environ

from discord import Intents

from src.Client.Client import Client
from src.Command.CommandManager import CommandManager


class Controller:

    def __init__(self):
        self.token = environ.get("DISCORD_TOKEN")

        if not self.token:
            print("No token provided")
            exit(1)

        self.client = Client(self, intents=Intents.all())
        self.commandManager = CommandManager(self.client)

        self.registerListeners()

    def registerListeners(self):
        pass

    def run(self):
        try:
            self.client.run(self.token, reconnect=True)
        except Exception as error:
            print(f"Error: {error}")
            exit(1)
