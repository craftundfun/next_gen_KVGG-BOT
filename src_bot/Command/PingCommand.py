import discord
from discord import Interaction

from src_bot.Command.BaseCommand import BaseCommand
from src_bot.Logging.Logger import Logger

logger = Logger("PingCommand")


class PingCommand(BaseCommand):

    def register(self):
        @self.tree.command(name="ping_command",
                           description="ping_description", guild=discord.Object(438689788585967616))
        async def ping(interaction: Interaction):
            await self.notifyBefore()

            # TODO dont send response here
            await interaction.response.send_message("Pong!")

            await self.notifyAfter()

        # TODO: maybe let that handle the CommandManager
        logger.debug("Registered command: ping")
