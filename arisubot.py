import discord
from discord.ext import commands, tasks
import datetime
import pytz
import tracemalloc
import random
import asyncio

# 봇 토큰과 채널 ID

TOKEN = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
MCHID = 1266916147639615639 

# 인텐트 설정

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 숫자야구

class NumberBaseballGame:
    def __init__(self):
        self.reset_game()

    def generate_secret_number(self):
        return ''.join(random.sample('123456789', 3))

    def reset_game(self):
        self.secret_number = None
        self.guesses = []
        self.game_active = False
        self.attempts = 0

    def start_game(self):
        self.secret_number = self.generate_secret_number()
        self.guesses = []
        self.game_active = True
        self.attempts = 0

    def make_guess(self, guess):
        if len(guess) != 3 or len(set(guess)) != 3 or not guess.isdigit():
            return "3자리 숫자를 입력해야 합니다!"

        self.guesses.append(guess)
        self.attempts += 1

        if guess == self.secret_number:
            self.game_active = False
            return f"와아~ 정답이에요! 답은 {game.secret_number}! {self.attempts}회 만에 맞혔습니다!"
        
        strikes, balls = self.calculate_strikes_and_balls(guess)
        return f"{guess} : {strikes}S {balls}B"
    
    def calculate_strikes_and_balls(self, guess):
        strikes = sum(1 for a, b in zip(guess, self.secret_number) if a == b)
        balls = sum(1 for g in guess if g in self.secret_number) - strikes
        return strikes, balls

class NumberBaseball:
    def __init__(self):
        self.games = {}

    def get_game(self, user):
        if user not in self.games:
            self.games[user] = NumberBaseballGame()
        return self.games[user]

    async def start_game_interaction(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if game.game_active:
            await interaction.response.send_message("저와 이미 게임을 하고 있어요!")
        else:
            game.start_game()
            await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임이 시작되었습니다! \n`/숫자야구_추측` 명령어를 사용해 3자리 숫자를 맞혀보세요. \n`/숫자야구_규칙` 명령어로 게임 규칙을 볼 수 있습니다!")

    async def guess_number(self, interaction: discord.Interaction, guess: str):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
        else:
            result = game.make_guess(guess)
            await interaction.response.send_message(result)

    async def give_up(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기도 하는 법!")
        else:
            game.game_active = False
            await interaction.response.send_message(f"게임을 포기했습니다. 정답은 {game.secret_number}입니다! \n아리스랑 놀아주세요...")

# 숫자 맞히기

class NumberGuessingGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.secret_number = None
        self.attempts = 0
        self.game_active = False

    def start_game(self, min_number=1, max_number=100):
        self.secret_number = random.randint(min_number, max_number)
        self.attempts = 0
        self.game_active = True

    def make_guess(self, guess):
        self.attempts += 1
        guess = int(guess)
        if guess < self.secret_number:
            return "더 높아요!"
        elif guess > self.secret_number:
            return "더 낮아요!"
        else:
            self.game_active = False
            return f"와아~ 정답이에요! 답은 {game.secret_number}! {self.attempts}회 만에 맞혔습니다!"

class NumberGuessing:
    def __init__(self):
        self.games = {} 

    def get_game(self, user):
        if user.id not in self.games:
            self.games[user.id] = NumberGuessingGame()
        return self.games[user.id]

    async def start_game_interaction(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if game.game_active:
            await interaction.response.send_message("저와 이미 게임을 하고 있어요!")
        else:
            game.start_game()
            await interaction.response.send_message("뽜밤뽜밤-! 숫자 맞히기 게임이 시작되었습니다! \n`/숫자게임_추측` 명령어를 사용해 1부터 100까지의 숫자를 맞혀보세요.")

    async def guess_number(self, interaction: discord.Interaction, guess: str):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
        else:
            result = game.make_guess(guess)
            await interaction.response.send_message(result)

    async def give_up(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기도 하는 법!")
        else:
            game.game_active = False
            await interaction.response.send_message(f"게임을 포기했습니다. 정답은 {game.secret_number}입니다! \n아리스랑 놀아주세요...")

# 봇 클래스 정의

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False
        self.number_baseball = NumberBaseball()
        self.number_guessing = NumberGuessing()
        
    async def on_ready(self):
        print(f'봇이 로그인되었습니다: {self.user.name}')
        if not self.synced:
            await self.tree.sync()
            print("슬래시 명령어가 동기화되었습니다.")
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()

bot = MyBot()

# 환영 메시지

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
lock = asyncio.Lock()
tz = pytz.timezone('Asia/Seoul')

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

# 가위바위보

@bot.tree.command(name="가위바위보", description="아리스와 가위바위보를 합니다")
async def rock_paper_scissors(interaction: discord.Interaction):
    options = ['가위', '바위', '보']

    # 버튼 생성
    view = discord.ui.View()
    
    for option in options:
        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)
        button.callback = lambda i: button_callback(i, interaction.user)
        view.add_item(button)
    await interaction.response.send_message("안 내면 집니다!", view=view)

async def button_callback(interaction: discord.Interaction, user: discord.User):
    options = ['가위', '바위', '보']
    bot_choice = random.choice(options)
    user_choice = interaction.data['custom_id']
    
    result = ""
    
    if user_choice == bot_choice:
        result = f"비겼습니다. 한 판 더 해요! ( 당신 : {user_choice}, 아리스 : {bot_choice} )"
    elif (user_choice == '가위' and bot_choice == '보') or \
         (user_choice == '바위' and bot_choice == '가위') or \
         (user_choice == '보' and bot_choice == '바위'):
        result = f"아리스가 졌어요. 끄앙 ( 당신 : {user_choice}, 아리스 : {bot_choice} )"
    else: 
        result = f"아리스가 이겼습니다!! ( 당신 : {user_choice}, 아리스 : {bot_choice} )"

    await interaction.response.edit_message(content=result, view=None)

# 기본 명령어

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
        "[숫자야구 룰]\n \n아리스가 정한 3자리 숫자를 맞히는 게임입니다! \n숫자는 0부터 9까지의 서로 다른 숫자 3개이며 \n숫자와 위치가 전부 맞으면 S (스트라이크), \n숫자와 위치가 틀리면 B (볼) 입니다. \n \n예시를 들어볼까요? 제가 정한 숫자가 ‘123’이면\n456 : 0S 0B\n781 : 0S 1B\n130 : 1S 1B\n132 : 1S 2B\n123 : 3S 0B 입니다! \n \n아리스랑 같이 놀아요 끄앙")

@bot.tree.command(name="숫자야구", description="아리스와 숫자야구 게임을 시작합니다")
async def 숫자야구(interaction: discord.Interaction):
    await bot.number_baseball.start_game_interaction(interaction)

@bot.tree.command(name="숫자야구_추측", description="숫자야구 - 숫자를 추측합니다")
async def 숫자야구_추측(interaction: discord.Interaction, guess: str):
    await bot.number_baseball.guess_number(interaction, guess)

@bot.tree.command(name="숫자야구_포기", description="숫자야구 - 게임을 포기합니다")
async def 숫자야구_포기(interaction: discord.Interaction):
    await bot.number_baseball.give_up(interaction)

@bot.tree.command(name="숫자게임", description="아리스와 숫자 맞히기 게임을 시작합니다")
async def 숫자추측(interaction: discord.Interaction):
    await bot.number_guessing.start_game_interaction(interaction)

@bot.tree.command(name="숫자게임_추측", description="숫자게임 - 숫자를 추측합니다")
async def 숫자추측_추측(interaction: discord.Interaction, guess: str):
    await bot.number_guessing.guess_number(interaction, guess)

@bot.tree.command(name="숫자게임_포기", description="숫자게임 - 게임을 포기합니다")
async def 숫자추측_포기(interaction: discord.Interaction):
    await bot.number_guessing.give_up(interaction)

@bot.tree.command(name="로또", description="아리스가 로또 번호를 골라줍니다")
async def 로또(interaction: discord.Interaction):
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    await interaction.response.send_message(f"이번 주 로또 번호는~ [ {', '.join(map(str, numbers))} ] 입니다! 당첨되면 저도...")

# 봇 실행

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
