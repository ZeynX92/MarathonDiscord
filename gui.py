from disnake.ext import commands


class GUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Тимка Дерзай :) Здесь должны быть списки и кнопки все как положено - подробно."""


def setup(bot):
    bot.add_cog(GUI(bot))
