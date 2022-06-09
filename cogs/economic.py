from disnake.ext import commands
from random import randint
from disnake import Member, Embed, Option, OptionType
from tools.insert import insert
from tools.json_work import read_json, write_json


class Economic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = read_json('cogs/database.json')

    @commands.slash_command(
        name='start_economic',
        description='Инициализировать экономику',
        options=[]
    )
    async def start_economic(self, inter):
        self.database = read_json('cogs/database.json')

        for member in inter.guild.members:
            post = {
                "guild": inter.guild.id,
                "member": member.id,
                "balance": randint(300, 500)
            }

            if str(post["guild"] + post["member"]) not in self.database.keys():
                insert(self.database, [post["guild"] + post["member"]], post)
                write_json('cogs/database.json', self.database)
                print('Новенький!')
            else:
                print(f'Уже есть: {member}')

        await inter.send(embed=Embed(title='Успех!', description='Экономика была запущена!'))

    @commands.slash_command(
        name='delete_economic',
        description='Удалить экономику',
        options=[]
    )
    async def delete_economic(self, inter):
        self.database = read_json('cogs/database.json')

        for member in inter.guild.members:
            if str(inter.guild.id + member.id) in self.database.keys():
                del self.database[str(inter.guild.id + member.id)]
                write_json('cogs/database.json', self.database)
                print('Удалил!')
            else:
                print(f'Уже неть: {member}')

        await inter.send(embed=Embed(title='Успех!', description='Экономика была удалена!'))

    @commands.slash_command(
        name='work',
        description='Условно "поработать" и получить игровую валюту',
        options=[]
    )
    async def work(self, inter):
        self.database = read_json('cogs/database.json')

        inc = randint(100, 300)

        self.database[str(inter.guild.id + inter.author.id)]["balance"] += inc

        write_json('cogs/database.json', self.database)

        await inter.send(embed=Embed(title='Хорошо поработали!', description=f'Вы заработали {inc} монеток'))

    @commands.slash_command(
        name='pay',
        description='Перевести деньги другому пользователю',
        options=[
            Option(
                name='member',
                description='Пользователь которому надо перевести деньги',
                type=OptionType.user,
                required=True
            ),
            Option(
                name='amount',
                description='Сумма которую хотите перевести',
                type=OptionType.integer,
                required=True
            )
        ]
    )
    async def pay(self, inter, member: Member, amount: int):
        self.database = read_json('cogs/database.json')

        if str(member.id + inter.guild.id) not in self.database.keys() or str(
                inter.author.id + inter.guild.id) not in self.database.keys():
            await inter.send(embed=Embed(title='Ошибка!', description='В базе данных нет таких пользователей!'))
            return

        if amount <= 0 or member.id == inter.author.id:
            await inter.send(embed=Embed(title='Ошибка!', description='Неверные аргументы!'))
            return

        self.database[str(inter.guild.id + inter.author.id)]["balance"] -= amount
        self.database[str(inter.guild.id + member.id)]["balance"] += amount

        write_json('cogs/database.json', self.database)

        await inter.send(embed=Embed(title='Перевод успешен!',
                                     description=f'Вы перевели {amount} монеток пользователю {member.mention}'))


def setup(bot):
    bot.add_cog(Economic(bot))
