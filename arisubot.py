import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import random
import pytz

# 환경 변수에서 봇 토큰 불러오기
TOKEN = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
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
        print(f'봇이 로그인되었습니다: {self.user}')
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        scheduled_task.start()
        self.load_cogs()

    def load_cogs(self):
        try:
            self.load_extension('number_baseball')
            self.load_extension('number_guessing_game')
            print("Cogs loaded successfully.")
        except Exception as e:
            print(f"Failed to load cogs: {e}")

bot = MyBot()

# 채널에 메시지 전송
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(MCHID)
    if channel:
        await channel.send('인간이 이곳에 온 것은 수천 년 만이군...')
    else:
        print('채널을 찾을 수 없습니다.')

# 예약된 메시지 전송 작업
schedule_times_messages = [
    ('19:00', '아리스랑 놀아주세요!'),
]

@tasks.loop(minutes=1)
async def scheduled_task():
    try:
        now = datetime.datetime.now(tz)
        current_time = now.strftime('%H:%M')
        print(f'[DEBUG] 현재 시각: {current_time}')
        
        for time_str, message in schedule_times_messages:
            if current_time == time_str:
                print('[DEBUG] 지정된 시각입니다.')
                channel = bot.get_channel(MCHID)
                
                if channel:
                    await channel.send(message)
                    print('[DEBUG] 메시지 전송 성공')
                else:
                    print('[ERROR] 채널을 찾을 수 없습니다.')
                break
        else:
            print('[DEBUG] 지정된 시각이 아닙니다.')
    except Exception as e:
        print(f'[ERROR] 오류 발생: {e}')

# 숫자야구 게임
class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name='숫자야구', description="아리스와 숫자야구 게임을 시작합니다")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
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
            await interaction.response.send_message(f"정답입니다! {self.games[interaction.channel.id]['attempts']}회 만에 맞췄어요!")
            del self.games[interaction.channel.id]
        else:
            await interaction.response.send_message(f"{guess} : {result}")

    @app_commands.command(name='포기_숫자야구', description="숫자야구 - 게임을 포기합니다")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기할 수 있습니다!")
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

# 숫자 맞추기 게임
class NumberGuessingGameBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name='숫자게임', description="숫자 맞추기 게임을 시작합니다")
    async def start_guessing_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
            return
        self.games[interaction.channel.id] = {
            'number': random.randint(1, 100),
            'attempts': 0
        }
        await interaction.response.send_message("숫자 맞추기 게임이 시작되었습니다! 1부터 100 사이의 숫자를 맞춰보세요. `/숫자게임_추측` 명령어를 사용하여 숫자를 입력해주세요.")

    @app_commands.command(name='숫자게임_추측', description="숫자 맞추기 - 숫자를 추측합니다")
    async def guess_number(self, interaction: discord.Interaction, guess: int):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자게임` 명령어로 게임을 시작해보세요!")
            return
        number = self.games[interaction.channel.id]['number']
        self.games[interaction.channel.id]['attempts'] += 1
        if guess < number:
            await interaction.response.send_message("더 높은 숫자입니다!")
        elif guess > number:
            await interaction.response.send_message("더 낮은 숫자입니다!")
        else:
            attempts = self.games[interaction.channel.id]['attempts']
            await interaction.response.send_message(f"정답입니다! {attempts}회 만에 맞췄어요!")
            del self.games[interaction.channel.id]

# 봇에 코그 추가
bot.add_cog(NumberBaseballBot(bot))
bot.add_cog(NumberGuessingGameBot(bot))

# 봇 실행
bot.run(TOKEN)
