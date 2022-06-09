import os
import config

from disnake.ext import commands
from disnake.flags import Intents

if config.debug:
    bot = commands.Bot(command_prefix="!", test_guilds=config.test_guilds, intents=Intents.all())
else:
    bot = commands.Bot(command_prefix="!", sync_commands_debug=True, intents=Intents.all())


@bot.event
async def on_ready():
    """
    |-ая ступень: сообщение о запуске
    print("Готов к Труду и Обороне!")
    """

    # ||-ая ступень: загрузчик когов

    print(f"Загружаю коги...")
    print("---------------")

    for name in os.listdir('./cogs'):
        if name.endswith('.py'):
            bot.load_extension(f'cogs.{name[:-3]}')
            print(f'Ког {name} был загружен.')

    print("---------------")
    print("Загрузил все коги!")


# |-ая ступень: префиксная команда эхо
@bot.command()
async def echo(ctx, *, echo_value):
    if ctx.author.id in config.devs:
        await ctx.send(echo_value)


# ||-ая ступень: команды для работы с когами
@bot.command()
async def load(ctx, extension):
    if ctx.author.id in config.devs:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Загружаю ког...")


@bot.command()
async def unload(ctx, extension):
    if ctx.author.id in config.devs:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Выгружаю ког...")


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id in config.devs:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Перезагружаю ког...")


bot.run(config.token)
