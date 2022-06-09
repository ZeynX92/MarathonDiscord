from disnake import PermissionOverwrite, Embed, TextChannel, OptionType, Option
from disnake.ext import commands


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.slash_command(
        name='create_channel',
        description='Cоздать канал',
        options=[
            Option(
                name='name',
                description='Название канала',
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def create_channel(self, inter, name: str):
        channel = await inter.guild.create_text_channel(name)

        await channel.send(embed=Embed(title='Успех!', description='Канал создан!'))

    @commands.slash_command(
        name='delete_channel',
        description='Удалить канал',
        options=[
            Option(
                name='channel',
                description='Канал, который надо удалить',
                type=OptionType.channel,
                required=True
            )
        ]
    )
    async def delete_channel(self, inter, channel: TextChannel):
        await channel.delete()

        await inter.send(embed=Embed(title='Успех!', description='Канал удален!'))

    @commands.slash_command(
        name='create_private',
        description='Создать приватный канал',
        options=[]
    )
    async def create_private(self, inter):
        overwrites = {
            inter.guild.default_role: PermissionOverwrite(view_channel=False),
            inter.guild.me: PermissionOverwrite(view_channel=True)
        }

        channel = await inter.guild.create_text_channel('secret', overwrites=overwrites)

        await channel.send(embed=Embed(title='Успех!', description='Приватный канал создан!'))


def setup(bot):
    bot.add_cog(Channels(bot))
