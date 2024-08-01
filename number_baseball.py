import discord
from discord import app_commands
from discord.ext import commands
import random

class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name='숫자야구', description="아리스와 숫자야구 게임을 시작합니다")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("저와 이미 게임을 하는 중입니다!")
            return
        self.games[interaction.channel.id] = {
            'number': self.generate_number(),
            'attempts': 0
        }
        await interaction.response.send_message("숫자야구 게임이 시작되었습니다! \n`/추측_숫자야구` 명령어를 사용해, 3자리 숫자를 맞춰보세요. \n`/숫자야구_규칙` 명령어로 게임 규칙을 볼 수 있습니다!")

    @app_commands.command(name='추측_숫자야구', description="숫자야구 - 숫자를 추측합니다")
    async def guess_number(self, interaction: discord.Interaction, guess: str):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자야구` 명령어로 게임을 시작해보세요!")
            return
        if len(guess) != 3 or not guess.isdigit():
            await interaction.response.send_message("3자리 숫자를 입력해야 합니다!")
            return
        result = self.check_guess(self.games[interaction.channel.id]['number'], guess)
        self.games[interaction.channel.id]['attempts'] += 1
        if result == "3S0B":
            await interaction.response.send_message(f"뽜밤뽜밤-! 정답입니다! {self.games[interaction.channel.id]['attempts']}회 만에 맞췄어요!")
            del self.games[interaction.channel.id]
        else:
            await interaction.response.send_message(f"{guess} : {result}")

    @app_commands.command(name='포기_숫자야구', description="숫자야구 - 게임을 포기합니다")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다.")
            return
        del self.games[interaction.channel.id]
        await interaction.response.send_message("게임을 포기했습니다. 아리스랑 놀아주세요...")

    def generate_number(self):
        while True:
            number = ''.join(random.sample('123456789', 3))
            if len(set(number)) == 3:
                return number

    def check_guess(self, number, guess):
        s = sum(n == g for n, g in zip(number, guess))
        b = sum(min(number.count(d), guess.count(d)) for d in set(guess)) - s
        return f"{s}S{b}B"

async def setup(bot):
    await bot.add_cog(NumberBaseballBot(bot))
