from discord.app_commands import CommandTree


class Command:
    def __init__(self, tree: CommandTree):
        self.tree = tree
        self.register()

    def register(self):
        raise NotImplementedError("Subclasses must implement the register method")