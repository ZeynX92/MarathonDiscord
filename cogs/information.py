from disnake.ext import commands
from disnake import Option, OptionType, Embed, Member


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="user_info",
        description="Выводит информацию о пользователе",
        options=[
            Option(
                name="member",
                description="Участник который будет кикнут",
                type=OptionType.user,
                required=False
            )
        ]
    )
    async def user_info(self, inter, member: Member = None):
        if member:
            info_embed = Embed(
                title=f'Информация о пользователе {member.name}'
            )
            info_embed.add_field('Дата регистрации:', f'<t:{int(member.created_at.timestamp())}>', inline=False)
            info_embed.add_field('Статус:', member.desktop_status)
            info_embed.add_field('Дата вступления на сервер:', f'<t:{int(member.joined_at.timestamp())}>',
                                 inline=False)
            info_embed.add_field('Наивысшая роль:', member.top_role.mention, inline=False)

            await inter.send(embed=info_embed)
        else:
            info_embed = Embed(
                title=f'Информация о пользователе {inter.author.name}'
            )
            info_embed.add_field('Дата регистрации:', f'<t:{int(inter.author.created_at.timestamp())}>', inline=False)
            info_embed.add_field('Статус:', inter.author.desktop_status)
            info_embed.add_field('Дата вступления на сервер:', f'<t:{int(inter.author.joined_at.timestamp())}>',
                                 inline=False)
            info_embed.add_field('Наивысшая роль:', inter.author.top_role.mention, inline=False)

            await inter.send(embed=info_embed)

    @commands.slash_command(
        name='guild_info',
        description='Информация о сервере',
        options=[]
    )
    async def guild_info(self, inter):
        info_embed = Embed(
            title=f'Информация о сервере: {inter.guild.name}'
        )

        info_embed.add_field('Дата создания:', f'<t:{int(inter.guild.created_at.timestamp())}>', inline=False)
        info_embed.add_field('Количество учатников:', inter.guild.member_count, inline=False)
        info_embed.add_field('Владелец:', inter.guild.owner.mention, inline=False)
        info_embed.add_field('Количество стикеров:', len(inter.guild.stickers), inline=False)

        await inter.send(embed=info_embed)


def setup(bot):
    bot.add_cog(Information(bot))
