from discord.app_commands import CommandTree


class CommandManager:
    tree: CommandTree = None

    def __init__(self, client):
        self.client = client
        self.tree = CommandTree(client)
        self.commands = []

    def add_command(self, command_class):
        command = command_class(self.tree)
        self.commands.append(command)

    async def syncCommands(self):
        await self.tree.sync(guild=self.client.get_guild(438689788585967616))

    async def removeCommands(self):
        self.tree.clear_commands(guild=self.client.get_guild(438689788585967616))

        await self.tree.sync(guild=self.client.get_guild(438689788585967616))
