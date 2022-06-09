import disnake
import asyncio
from disnake.ext import commands
from datetime import timedelta
from disnake import Option, OptionType, Embed, Member
from tools.getseconds import getseconds


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.slash_command(
        name="kick",
        description="Кикает участника",
        options=[
            Option(
                name="member",
                description="Участник который будет кикнут",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="Причина кика",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def kick(self, ctx, member: Member, reason: str):
        if member.id == ctx.author.id:
            await ctx.send(embed=Embed(title='❌ Ошибка!',
                                       description='Нельзя кикнуть самого себя!',
                                       color=disnake.Colour.red()))
            return

        embed_kick_wait = Embed(
            title='Кик',
            description=f'Ожидание кика...'
        )

        embed_kick = Embed(
            title='Кик!',
            description=f'{member.mention} был кикнут! По причине: {reason}'
        )

        await ctx.send(embed=embed_kick_wait)

        await member.kick(reason=reason)

        await ctx.send(embed=embed_kick)

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.slash_command(
        name="ban",
        description="Банит участника",
        options=[
            Option(
                name="member",
                description="Участник который будет забанен",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="time",
                description="Время, которое участник проведет в бане",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="reason",
                description="Причина бана",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def ban(self, ctx, member: Member, time: str, reason: str):
        if not getseconds(time):
            await ctx.send(embed=Embed(title='❌ Ошибка!',
                                       description='Неправильные аргументы!',
                                       color=disnake.Colour.red()),
                           ephemeral=True)
            return

        if member.id == ctx.author.id:
            embed = Embed(
                title='❌ Ошибка!',
                description='Вы не можете забанить сами себя!',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_ban_wait = Embed(
            title='Бан!',
            description=f'Подготовка к бану...'
        )

        embed_ban = Embed(
            title='Бан!',
            description=f'{member} был забанен на {time}! По причине: {reason}.'
        )

        await ctx.send(embed=embed_ban_wait)

        await member.ban(reason=f'Banned by {ctx.author} by reason {reason} on {time}')

        await ctx.send(embed=embed_ban)

        await member.unban(reason='Истекло время наказания.')

        embed_ban_unban = Embed(
            title='Разбан!',
            description=f'{member} был разбанен!'
        )

        await ctx.send(embed=embed_ban_unban)

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.slash_command(
        name="mute",
        description="Мутит участника",
        options=[
            Option(
                name="member",
                description="Участник который получит мут",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="time",
                description="Время которое участник проведет в муте",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="reason",
                description="Причина мута",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def mute(self, ctx, member: disnake.Member, time: str, reason: str):
        if not getseconds(time):
            await ctx.send(embed=Embed(title='❌ Ошибка!',
                                       description='Неправильные аргументы!',
                                       color=disnake.Colour.red()),
                           ephemeral=True)
            return

        if member.id == ctx.author.id:
            await ctx.send(embed=Embed(title='❌ Ошибка!',
                                       description='Вы не можете замьютить сами себя!',
                                       color=disnake.Colour.red()),
                           ephemeral=True)
            return

        delta = timedelta(
            seconds=getseconds(time)
        )

        await ctx.guild.timeout(user=member, duration=delta,
                                reason=f'Timeouted by {ctx.author} by reason {reason} on {time}')

        embed_mute = Embed(
            title='Мут!',
            description=f'{member.mention} был замьючен за {reason}.'
        )

        embed_mute_unmute = Embed(
            title='Размут!',
            description=f'{member} был размучен!'
        )

        await ctx.send(embed=embed_mute)

        await asyncio.sleep(getseconds(time))

        await ctx.send(embed=embed_mute_unmute)

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.slash_command(
        name="clear",
        description="Очищает чат от сообщений",
        options=[
            Option(
                name="count",
                description="Сколько сообщений будет удалено",
                type=OptionType.integer,
                required=True
            )
        ]
    )
    async def clear(self, ctx, count: int):
        if not (1 <= count <= 500):
            embed = Embed(title="❌ Ошибка!",
                          description='Ограничение!')
            await ctx.send(embed=embed)
            return

        await ctx.channel.purge(limit=count)

        await ctx.send(embed=Embed(title='✅ Успех!',
                                   description=f'Было удалено {count} сообщений!',
                                   color=disnake.Colour.green()))


def setup(bot):
    bot.add_cog(Moderator(bot))
