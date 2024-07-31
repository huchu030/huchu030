import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import time
import random
import asyncio
import pytz
import tracemalloc



token = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
tchid = 1267153846258499675
mchid = 1266916147639615639

tz = pytz.timezone('Asia/Seoul')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)



class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(intents=intents, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.add_cog(NumberBaseballBot(self))
        self.synced = False


@bot.event
async def on_ready():
    print(f'봇이 로그인되었습니다: {bot.user}')
    scheduled_task.start()
    tracemalloc.start()
    await bot.tree.sync()

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(mchid)
    if channel:
        await channel.send('인간이 이곳에 온 것은 수천 년 만이군...')
    else:
        print('...')



schedule_times_messages = [
    ('19:00', '아리스랑 놀아주세요!'),]

@tasks.loop(minutes=1)
async def scheduled_task():
    try:
        now = datetime.datetime.now(tz)
        current_time = now.strftime('%H:%M')
        print(f'[DEBUG] 현재시각:{current_time}')
        
        for time_str, message in schedule_times_messages:
            if current_time == time_str:
                print('[DEBUG] 지정시각이당')
                channel = bot.get_channel(mchid)
                
                if channel:
                    await channel.send(message)
                    print(f'[DEBUG] 성공')
                else:
                    print(f'[ERROR] 채널없어')

                break
        else:
            print('[DEBUG] 지정시각아니야')
    except Exception as e:
        print(f'[ERROR] 오류 발생: {e}')


class SlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name='테스트', description="testing")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("tested", ephemeral=False)



@bot.tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!", ephemeral=False) 


@bot.tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def 로봇주제에(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!", ephemeral=False)


@bot.tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def 밥(interaction: discord.Interaction):
    await interaction.response.send_message("응..? 아리스는 건전지를 먹지 않습니다!", ephemeral=False)


class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print(f'Logged in as {self.bot.user}')

    @discord.app_commands.command(name='숫자야구', description="아리스와 숫자야구 게임을 합니다.")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
            return
        self.games[interaction.channel.id] = {
            'number': self.generate_number(),
            'attempts': 0
        }
        await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임이 시작되었습니다! `/추측` 명령어를 사용해, 3자리 숫자를 맞춰보세요~")

    @discord.app_commands.command(name='추측', description="숫자야구 - 숫자를 추측합니다.")
    async def guess_number(self, interaction: discord.Interaction, guess: str):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자야구` 명령어로 게임을 시작해보세요!")
            return
        if len(guess) != 3 or not guess.isdigit():
            await interaction.response.send_message("3자리 숫자를 입력해야돼요!")
            return
        result = self.check_guess(self.games[interaction.channel.id]['number'], guess)
        self.games[interaction.channel.id]['attempts'] += 1
        

        if result == "3S0B":
            await interaction.response.send_message(f"와아~ 정답입니다! {self.games[interaction.channel.id]['attempts']}회 만에 맞췄어요!")
            del self.games[interaction.channel.id]
        else:
            await interaction.response.send_message(f"{guess} : {result}")

    @discord.app_commands.command(name='포기', description="숫자야구 - 게임을 포기합니다.")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다.")
            return
        del self.games[interaction.channel.id]
        await interaction.response.send_message("게임을 포기했습니다. 아리스랑 놀아주세요..")

    def generate_number(self):
        while True:
            number = ''.join(random.sample('123456789', 3))
            if len(set(number)) == 3:
                return number
    def check_guess(self, number, guess):
        s = sum(n == g for n, g in zip(number, guess))
        b = sum(min(number.count(d), guess.count(d)) for d in set(guess)) - s
        return f"{s}S{b}B"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def main():
    await bot.add_cog(NumberBaseballBot(bot))
    await bot.start(token)
if __name__ == "__main__":
    asyncio.run(main())

         


@bot.tree.command(name='가위바위보', description="아리스와 가위바위보를 합니다")
@app_commands.describe(choice="가위, 바위, 보 중 하나를 선택하세요.")
@app_commands.choices(
    choice=[
        app_commands.Choice(name="가위", value="가위"),
        app_commands.Choice(name="바위", value="바위"),
        app_commands.Choice(name="보", value="보")])
async def rock_paper_scissors(interaction: discord.Interaction, choice: str):
    ranNum = (random.randint(1,3))
    if choice == '가위':
        if ranNum == 1:
            await interaction.response.send_message("(가위) 비겼습니다. 한 판 더!")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 아리스가 이겼습니다!!")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 아리스가 졌어요. 끄앙")
    elif choice == '바위':
        if ranNum == 1:
            await interaction.response.send_message("(가위) 아리스가 졌어요. 끄앙")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 비겼습니다. 한 판 더!")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 아리스가 이겼습니다!!")
    elif choices == '보':
        if ranNum == 1:
            await interaction.response.send_message("(가위) 아리스가 이겼습니다!!")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 아리스가 졌어요. 끄앙")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 비겼습니다. 한 판 더!")


bot.loop.create_task(setup_bot())
bot.run(token)
