import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import random
import pytz
import tracemalloc
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
        print(f'봇이 로그인되었습니다: {self.user}')
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()
        await self.add_cogs()
        
    async def add_cogs(self):
        await self.add_cog(NumberBaseballBot(self))
        await self.add_cog(NumberGuessingGameBot(self))

bot = MyBot()

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

# 숫자야구 게임
class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name='숫자야구', description="아리스와 숫자야구 게임을 합니다")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel_id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
            return
        self.games[interaction.channel_id] = {
            'number': self.generate_number(),
            'attempts': 0
        }
        await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임이 시작되었습니다! \n`/추측_숫자야구` 명령어를 사용해, 3자리 숫자를 맞춰보세요. \n`/숫자야구_규칙` 명령어를 사용하면 게임 규칙을 볼 수 있습니다!")

    @app_commands.command(name='추측_숫자야구', description="숫자야구 - 숫자를 추측합니다")
    async def guess_number(self, interaction: discord.Interaction, guess: str):
        if interaction.channel_id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자야구` 명령어로 게임을 시작해보세요!")
            return
        if len(guess) != 3 or not guess.isdigit():
            await interaction.response.send_message("3자리 숫자를 입력해야돼요!")
            return
        result = self.check_guess(self.games[interaction.channel_id]['number'], guess)
        self.games[interaction.channel_id]['attempts'] += 1
        if result == "3S0B":
            await interaction.response.send_message(f"와아~ 정답입니다! {self.games[interaction.channel_id]['attempts']}회 만에 맞췄어요!")
            del self.games[interaction.channel_id]
        else:
            await interaction.response.send_message(f"{guess} : {result}")

    @app_commands.command(name='포기_숫자야구', description="숫자야구 - 게임을 포기합니다")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel_id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기하는 법!")
            return
        del self.games[interaction.channel_id]
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

    @app_commands.command(name='숫자게임', description="아리스와 숫자 맞추기 게임을 합니다")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel_id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다..!")
            return
        self.games[interaction.channel_id] = {
            'target_number': random.randint(1, 100),
            'attempts': 0}
        await interaction.response.send_message("뽜밤뽜밤-! 숫자 맞추기 게임이 시작되었습니다! \n`/추측_숫자게임` 명령어를 사용해, 1부터 100 사이의 숫자를 맞춰보세요.")

    @app_commands.command(name='추측_숫자게임', description="숫자게임 - 숫자를 추측합니다")
    async def guess_number(self, interaction: discord.Interaction, guess: int):
        if interaction.channel_id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. `/숫자게임` 명령어로 게임을 시작해보세요!")
            return

        game = self.games[interaction.channel_id]
        game['attempts'] += 1

        if guess < game['target_number']:
            await interaction.response.send_message("더 높아요!")
        elif guess > game['target_number']:
            await interaction.response.send_message("더 낮아요!")
        else:
            await interaction.response.send_message(f"와아~ 정답입니다! 숫자는 {game['target_number']}였어요. 총 {game['attempts']}번 시도했습니다.")
            del self.games[interaction.channel_id]

    @app_commands.command(name='포기_숫자게임', description="숫자게임 - 게임을 포기합니다")
    async def surrender_game(self, interaction: discord.Interaction):
        if interaction.channel_id not in self.games:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기하는 법!")
            return
        del self.games[interaction.channel_id]
        await interaction.response.send_message("게임을 포기했습니다. 아리스랑 놀아주세요...")

# 기본 슬래시 명령어


@bot.tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!", ephemeral=False)

@bot.tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def 로봇주제에(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!", ephemeral=False)

@bot.tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def 밥(interaction: discord.Interaction):
    await interaction.response.send_message("응..? 아리스는 건전지를 먹지 않습니다!", ephemeral=False)

@bot.tree.command(name='쓰담', description="아리스의 인공 단백질 피부가 따뜻해집니다")
async def 쓰담(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 행복합니다..", ephemeral=False)

@bot.tree.command(name='숫자야구_규칙', description="아리스가 숫자야구의 규칙을 설명해줍니다")
async def 숫자야구_규칙(interaction: discord.Interaction):
    await interaction.response.send_message(
        "[숫자야구 룰]\n \n아리스가 정한 3자리 숫자를 맞히는 게임입니다! 사용되는 숫자는 0부터 9까지 서로 다른 숫자 3개이며 숫자와 위치가 전부 맞으면 S (스트라이크), 숫자와 위치가 틀리면 B (볼) 입니다. \n \n예시를 들어볼까요? 제가 정한 숫자가 ‘123’이면\n456 : 0S0B\n781 : 0S1B\n130 : 1S1B\n132 : 1S2B\n123 : 3S0B 입니다! \n아리스랑 같이 놀아요 끄앙", ephemeral=False
    )


# 봇 실행
bot.run(TOKEN)
