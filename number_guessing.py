import discord
from discord import app_commands
from discord.ext import commands
import random

class NumberGuessingGameBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name='숫자게임', description="아리스와 숫자 맞추기 게임을 시작합니다")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
            return
        self.games[interaction.channel.id] = {
            'target_number': random.randint(1, 100),
            'attempts': 0}
        await interaction.response.send_message("숫자 맞추기 게임이 시작되었습니다! \n`/추측_숫자게임` 명령어를 사용해, 1부터 100 사이의 숫자를 맞춰보세요.")

    @app_commands.command(name='추측_숫자게임', description="숫자게임 - 숫자를 추측합니다")
    async def guess_number(self, interaction: discord.Interaction, guess: int):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자게임` 명령어로 게임을 시작해보세요!")
            return

        game = self.games[interaction.channel.id]
        game['attempts'] += 1

        if guess < game['target_number']:
            await interaction.response.send_message("더 높아요!")
        elif guess > game['target_number']:
            await interaction.response.send_message("더 낮아요!")
        else:
            await interaction.response.send_message(f"정답입니다! 숫자는 {game['target_number']}였어요. 총 {game['attempts']}번 시도했습니다.")
            del self.games[interaction.channel.id]

    @app_commands.command(name='포기_숫자게임', description="숫자게임 - 게임을 포기합니다")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기할 수 있습니다!")
            return
        del self.games[interaction.channel.id]
        await interaction.response.send_message("게임을 포기했습니다. 아리스랑 놀아주세요...")

async def setup(bot):
    await bot.add_cog(NumberGuessingGameBot(bot))
