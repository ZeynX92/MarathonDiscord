from disnake.ext import commands
import disnake


# класс для кнопок
class ButtonsView(disnake.ui.View):
    def __init__(self):
        super(ButtonsView, self).__init__(timeout=None)

    @disnake.ui.button(label='Забанить', style=disnake.ButtonStyle.red)
    async def ban_member_button(self, button: disnake.ui.Button,
                                inter: disnake.MessageInteraction):
        await inter.send('Ты хочешь себя забанить? Ха-ха-ха!', ephemeral=True)

    @disnake.ui.button(label='Кикнуть', style=disnake.ButtonStyle.blurple)
    async def kick_member_button(self, button: disnake.ui.Button,
                                 inter: disnake.MessageInteraction):
        await inter.send('Кикнуть себя? Не смеши мои тапки', ephemeral=True)

    @disnake.ui.button(label='Предупреждение', style=disnake.ButtonStyle.green)
    async def warn_member_button(self, button: disnake.ui.Button,
                                 inter: disnake.MessageInteraction):
        await inter.send('Выдать себе варн? Ты нормальный?', ephemeral=True)

# создаем View класс для меню выбора
class SelectView(disnake.ui.View):
    def __init__(self):
        super(SelectView, self).__init__(timeout=None)
        
    @disnake.ui.select(placeholder='Выбери уже что-нибудь, семпай!', options=[
        disnake.SelectOption(
            label='Вода',
            value='water',
            description='Просто бутылка воды. Стоит 1$.'
        ),
        disnake.SelectOption(
            label='Бутерброд',
            value='eat',
            description='Бутерброд с маслом и сыром : ) Стоит 5$'
        )
    ])
    async def select_eat(self, select: disnake.ui.Select,
                         inter: disnake.MessageInteraction):
        if select.values[0] == 'water':
            await inter.send('Ты купил воду.', ephemeral=True)
        elif select.values[0] == 'eat':
            await inter.send('Ты купил бутерброд. Приятного аппетита ; )', ephemeral=True)

# модальное окно      
class ModalWindow(disnake.ui.Modal):
    def __init__(self):
        super(ModalWindow, self).__init__(title='Предложи идею нам!',
                                          components=[
                                              disnake.ui.TextInput(
                                                  label='Краткая суть',
                                                  placeholder='Изложи идею кратко, семпай!',
                                                  max_length=50,
                                                  min_length=5,
                                                  style=disnake.TextInputStyle.short,
                                                  custom_id='title'
                                              ),
                                              disnake.ui.TextInput(
                                                  label='Подробная идея',
                                                  placeholder='Можешь рассказать подробнее, нам всем очень интересно!',
                                                  max_length=1000,
                                                  min_length=30,
                                                  style=disnake.TextInputStyle.long,
                                                  custom_id='description'
                                              )
                                          ])

        async def callback(self, interaction: disnake.ModalInteraction):
            embed = disnake.Embed(
                title='Новая идея!'
            )
            for key, value in interaction.text_values:
                embed.add_field(name=key, value=value)

            await interaction.send(embed=embed)

        async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
            print(f'Ошибка в модальном окне: {error}')
            await inter.send(f'Произошла ошибка: ```{error}```', ephemeral=True)

class GUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Тимка Дерзай :) Здесь должны быть списки и кнопки все как положено - подробно."""

    @commands.slash_command()
    async def button(self, inter):
        """Высылает сообщение с кнопкой"""
        await inter.send('Нажми на кнопку ниже!', view=ButtonsView())

    @commands.slash_command()
    async def select(self, inter):
        """Высылает сообщение с меню выбора"""
        await inter.send('Выбери что-нибудь', view=SelectView())

    @commands.slash_command()
    async def modal(self, inter):
        """Высылает сообщение с модальным окном"""
        await inter.response.send_modal(modal=ModalWindow())

def setup(bot):
    bot.add_cog(GUI(bot))
