import discord
from discord import Interaction

from src.command.Command import Command


class PingCommand(Command):

    def register(self):
        @self.tree.command(name="ping", description="Pong!", guild=discord.Object(438689788585967616))
        async def ping(interaction: Interaction):
            await interaction.response.send_message("Pong!")