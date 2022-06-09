from disnake.ext import commands
from disnake import Member, Role, Option, OptionType, Embed, RawReactionActionEvent


class UserActivities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.slash_command(
        name='add_role',
        description='Добавить роль участнику',
        options=[
            Option(
                name='role',
                description='Роль, которую требуется выдать',
                type=OptionType.role,
                required=True
            ),
            Option(
                name='member',
                description='Участник, которому требуется выдать роль',
                type=OptionType.user,
                required=False
            )
        ]
    )
    async def add_role(self, inter, role: Role, member: Member = None):
        if not member:
            member = inter.author

        if role in member.roles:
            await inter.send(embed=Embed(title='❌ Ошибка!', description='Данная роль уже есть у пользователя!'))
        else:
            await member.add_roles(role, reason=f'Command used by {inter.author}')

            await inter.send(
                embed=Embed(title='Успех!',
                            description=f'Роль {role.mention} была выдана пользователю {member.mention}'))

    @commands.slash_command(
        name='remove_role',
        description='Забирает роль у пользователя',
        options=[
            Option(
                name='role',
                description='Роль, которую требуется удалить',
                type=OptionType.role,
                required=True
            ),
            Option(
                name='member',
                description='Участник, которому требуется удалить роль',
                type=OptionType.user,
                required=False
            )
        ]
    )
    async def remove_role(self, inter, role: Role, member: Member = None):
        if not member:
            member = inter.author

        if role not in member.roles:
            await inter.send(embed=Embed(title='❌ Ошибка!', description='Данной роли уже нет у пользователя!'))
        else:
            await member.remove_roles(role, reason=f'Command used by {inter.author}')

            await inter.send(
                embed=Embed(title='Успех!',
                            description=f'Роль {role.mention} была удалена у пользователя {member.mention}'))

    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.slash_command(
        name='edit_nick',
        description='Изменяет НИК пользователя',
        options=[
            Option(
                name='new_nick',
                description='Новый НИК',
                type=OptionType.string,
                required=True
            ),
            Option(
                name='member',
                description='Участник чей НИК надо изменить',
                type=OptionType.user,
                required=False
            )
        ]
    )
    async def edit_nick(self, inter, new_nick: str, member: Member = None):
        if not member:
            member = inter.author

        await member.edit(nick=new_nick)

        await inter.send("НИК успещно изменен!", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        print(f'Событие: {payload.event_type}')
        print(f'Сервер: {payload.guild_id}')
        print(f'Пользователь: {payload.user_id}')
        print(f'Реакция: {payload.emoji}')
        print(f'Сообщение: {payload.channel_id}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        print(f'Событие: {payload.event_type}')
        print(f'Сервер: {payload.guild_id}')
        print(f'Пользователь: {payload.user_id}')
        print(f'Реакция: {payload.emoji}')
        print(f'Сообщение: {payload.channel_id}')


def setup(bot):
    bot.add_cog(UserActivities(bot))
