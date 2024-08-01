import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import pytz
import tracemalloc
import random
import asyncio

# 봇 토큰과 채널 ID
TOKEN = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"  # 실제 토큰으로 교체하세요
MCHID = 1266916147639615639

# 타임존 설정
tz = pytz.timezone('Asia/Seoul')

# 인텐트 설정
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# 봇 클래스 정의
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False

    async def on_ready(self):
        print(f'봇이 로그인되었습니다: {self.user.name}')
        if not self.synced:
            await self.tree.sync()
            print("슬래시 명령어가 동기화되었습니다.")
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()
        await self.add_cogs()

    async def add_cogs(self):
        await bot.add_cog(NumberBaseballBot(self))

bot = MyBot()
lock = asyncio.Lock()

# 채널에 메시지 전송
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(MCHID)
    if channel:
        await channel.send('인간이 이곳에 온 것은 수천 년 만이군...')
    else:
        print('채널을 찾을 수 없습니다.')

# 알림 메시지
schedule_times_messages = [
    ('19:00', '아리스랑 놀아주세요!'),
]

@tasks.loop(minutes=1)
async def scheduled_task():
    async with lock:
        try:
            now = datetime.datetime.now(tz)
            current_time = now.strftime('%H:%M')
            print(f'[DEBUG] 현재시각: {current_time}')
        
            for time_str, message in schedule_times_messages:
                if current_time == time_str:
                    print('[DEBUG] 지정시각이당')
                    channel = bot.get_channel(MCHID)
                
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

# 기본 슬래시 명령어
@bot.tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!")

@bot.tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def 로봇주제에(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!")

@bot.tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def 밥(interaction: discord.Interaction):
    await interaction.response.send_message("응..? 아리스는 건전지를 먹지 않습니다!")

@bot.tree.command(name='쓰담', description="아리스의 인공 단백질 피부가 따뜻해집니다")
async def 쓰담(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 행복합니다..")

@bot.tree.command(name='숫자야구_규칙', description="아리스가 숫자야구의 규칙을 설명해줍니다")
async def 숫자야구_규칙(interaction: discord.Interaction):
    await interaction.response.send_message(
        "[숫자야구 룰]\n \n아리스가 정한 3자리 숫자를 맞히는 게임입니다! 사용되는 숫자는 0부터 9까지 서로 다른 숫자 3개이며 숫자와 위치가 전부 맞으면 S (스트라이크), 숫자와 위치가 틀리면 B (볼) 입니다. \n \n예시를 들어볼까요? 제가 정한 숫자가 ‘123’이면\n456 : 0S0B\n781 : 0S1B\n130 : 1S1B\n132 : 1S2B\n123 : 3S0B 입니다! \n아리스랑 같이 놀아요 끄앙")

# 숫자야구 게임 클래스
class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    def generate_number(self):
        digits = random.sample(range(10), 3)
        return ''.join(map(str, digits))

    def check_guess(self, secret, guess):
        strike = sum(1 for s, g in zip(secret, guess) if s == g)
        ball = sum(1 for g in guess if g in secret) - strike
        return strike, ball

    @app_commands.command(name="숫자야구", description="아리스와 숫자야구 게임을 시작합니다")
    async def 숫자야구(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.games:
            await interaction.response.send_message("저랑 이미 게임을 하고 있습니다!")
        else:
            secret_number = self.generate_number()
            self.games[user_id] = secret_number
            await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임이 시작되었습니다! \n`/숫자야구_추측` 명령어를 사용해, 3자리 숫자를 맞춰보세요. \n`/숫자야구_규칙` 명령어로 게임 규칙을 볼 수 있습니다!")

    @app_commands.command(name="숫자야구_추측", description="숫자야구 - 숫자를 추측합니다")
    async def 숫자야구_추측(self, interaction: discord.Interaction, guess: str):
        user_id = interaction.user.id
        if user_id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자야구` 명령어로 게임을 시작해보세요!")
        elif len(guess) != 3 or not guess.isdigit() or len(set(guess)) != 3:
            await interaction.response.send_message("3자리 숫자를 입력해야 합니다!")
        else:
            secret_number = self.games[user_id]
            strike, ball = self.check_guess(secret_number, guess)
            if strike == 3:
                await interaction.response.send_message(f"와아~ 정답입니다! {self.games[interaction.channel.id]['attempts']}회 만에 맞췄어요!")
                del self.games[user_id]
            else:
                await interaction.response.send_message(f"{strike}S {ball}B")

    @app_commands.command(name='숫자야구_포기', description="숫자야구 - 게임을 포기합니다")
    async def 숫자야구_포기(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
        else:
            secret_number = self.games.pop(user_id)
            await interaction.response.send_message("게임을 포기했습니다. 아리스랑 놀아주세요...")

# main 함수에 슬래시 명령어 동기화 추가

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
