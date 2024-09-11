import discord
from discord.ext import commands, tasks
import datetime
from datetime import datetime
import asyncio
import tracemalloc
import random
import pytz
from tokens import ttoken, MCHID, TCHID


# 인텐트 설정

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# 운세

class FortuneManager:
    def __init__(self):
        self.user_last_fortune_date = {}
        self.user_last_fortune = {}
        self.fortunes = [
            "오늘은 행운이 가득한 날입니다.",
            "조금 더 노력하면 큰 성과를 얻을 수 있을 것입니다.",
            "누군가가 당신에게 도움을 줄 것입니다.",
            "오늘은 도전 정신이 필요한 날입니다. 어려운 문제를 해결하는 기회로 삼으세요.",
            "오늘은 쉬어도 됩니다.",
            "인내와 끈기가 필요한 하루입니다. 힘든 일이 닥치더라도 나아가세요.",
            "소중한 사람과의 만남이 기다리고 있습니다.",
            "균형 잡힌 식사와 충분한 휴식이 필요한 날입니다. 몸과 마음을 돌보는 시간을 가지세요.",
            "예상치 못한 어려움이 올 수 있지만, 그것이 성장의 계기가 될 것입니다.",
            "소중한 사람과의 관계가 더욱 깊어질 수 있는 기회가 올 것입니다.",
            "감정 표현이 중요한 날입니다. 소중한 사람에게 당신의 진심을 전해보세요.",
            "활동적인 하루를 보내세요. 운동이나 산책으로 스트레스를 해소하는 것이 좋습니다.",
            "긍정적인 생각이 긍정적인 결과를 가져올 것입니다.",
            "오늘은 수능 만점이 나올 운세입니다!",
            "오늘의 행운의 색은 노란색입니다.",
            "오늘의 행운의 색은 보라색입니다.",
            "오늘의 행운의 색은 검정색입니다.",
            "오늘의 행운의 색은 빨간색입니다.",
            "오늘의 행운의 색은 파란색입니다.",
            "오늘의 행운의 색은 흰색입니다.",
            "회원님 오늘의 운(동계획)세(우기)는 상체입니다.",
            "회원님 오늘의 운(동계획)세(우기)는 하체입니다.",
            "오늘은 서브웨이를 드셔보세요. `/서브웨이`로 레시피를 추천받을 수 있습니다."
            ]

    def get_random_fortune(self):
        return random.choice(self.fortunes)

    def can_show_fortune(self, user_id):
        today = datetime.now().date()
        if user_id in self.user_last_fortune_date:
            last_date = self.user_last_fortune_date[user_id]
            return last_date < today
        return True

    def update_last_fortune_date(self, user_id):
        self.user_last_fortune_date[user_id] = datetime.now().date()

    def get_last_fortune(self, user_id):
        return self.user_last_fortune.get(user_id, None)

    def set_last_fortune(self, user_id, fortune):
        self.user_last_fortune[user_id] = fortune

# 31

class ThirtyOneGame:

    def start_game(self):
        self.game_active = True
        self.total = 0
        self.last_added = 0

    async def make_add(self, add, interaction):
        add = int(add)
        start = self.total
        self.total += add
        numbers_added = list(range(start, self.total))

        guild = interaction.guild
        user_nickname = get_user_nickname(guild, interaction.user.id)


        if 26 < self.total < 30:
            await interaction.response.send_message ("제가 이겼습니다. 예이~")
            self.game_active = False

        elif self.total == 30:
            await interaction.response.send_message ("...제가 졌습니다.")
            self.game_active = False

        else:
            await interaction.response.send_message (f"{user_nickname} : {numbers_added}")
            start = self.total
            bot_choice = random.randint(1,3)
            self.total += bot_choice
            numbers_added = list(range(start, self.total))
            await interaction.followup.send_message (f"토키 : {numbers_added}")


class ThirtyOne:
    def __init__(self):
        self.games = {} 

    def get_game(self, user):
        if user.id not in self.games:
            self.games[user.id] = ThirtyOneGame()
        return self.games[user.id]

    async def start_game_interaction(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if game.game_active:
            await interaction.response.send_message("저와 이미 게임을 하고 있습니다.")
        else:
            game.start_game()
            await interaction.response.send_message("베스킨라빈스 써리원~ \n"
                                                    "`/31`로 1부터 3까지의 숫자를 입력하세요.")

    async def add_number(self, interaction: discord.Interaction, add: str):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 저랑 놀아주세요.")
        else:
            if not add.isdigit() or not (1 <= int(add) <= 3):
                await interaction.response.send_message("1부터 3까지의 숫자만 입력할 수 있습니다.")
                return

            result = await game.make_add(add, interaction)

    async def give_up(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. `/31_시작`으로 게임을 시작해보세요.")
        else:
            game.game_active = False
            await interaction.response.send_message("게임을 포기했습니다. 저랑 그만 노실 건가요..?")




# 봇

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False
        self.fortune_manager = FortuneManager()
        self.ThirtyOne = ThirtyOne()
        
    async def on_ready(self):
        print(f'봇이 로그인되었습니다: {self.user.name}')
        if not self.synced:
            await self.tree.sync()
            print("슬래시 명령어가 동기화되었습니다.")
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()

bot = MyBot()

# 사용자 서버 닉네임 출력 함수        

def get_user_nickname(guild, user_id):
    member = guild.get_member(user_id)
    if member:
        return member.display_name
    return "Unknown"

# 알림 메시지

schedule_times_messages = [
    ('00:00', '잘 시간입니다. 좋은 꿈 꾸세요.'),
    ('08:00', '일어날 시간입니다. 아침밥도 드셔야 해요.'),
    ('12:00', '오늘의 점심은, 무엇인가요?'),
    ('16:00', "심심하지 않으신가요? 그럴 땐, `/도박`을 권장드립니다."),
    ('22:00', '오늘도 수고하셨습니다. 물론 저도요. 뿅뿅')
    ]
lock = asyncio.Lock()
tz = pytz.timezone('Asia/Seoul')

@tasks.loop(minutes=1)
async def scheduled_task():
    async with lock:
        try:
            now = datetime.now(tz)
            current_time = now.strftime('%H:%M')
            print(f'[DEBUG] 현재시각: {current_time}')
        
            for time_str, message in schedule_times_messages:
                if current_time == time_str:
                    print('[DEBUG] 지정시각입니다')
                    channel = bot.get_channel(MCHID)
                
                    if channel:
                        await channel.send(message)
                        print(f'[DEBUG] 성공')
                    else:
                        print(f'[ERROR] 채널이 없습니다')
                    break
            else:
                print('[DEBUG] 지정시각이 아닙니다.')
        except Exception as e:
            print(f'[ERROR] 오류 발생: {e}')





# 가위바위보

@bot.tree.command(name="가위바위보", description="토키와 가위바위보를 합니다")
async def rock_paper_scissors(interaction: discord.Interaction):
    options = ['가위', '바위', '보']
    view = discord.ui.View()
    
    for option in options:
        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)
        button.callback = lambda i: button_callback(i, interaction.user)
        view.add_item(button)
        
    await interaction.response.send_message("준비되시면, 말씀해 주세요.", view=view)

async def button_callback(interaction: discord.Interaction, user: discord.User):
    options = ['가위', '바위', '보']
    bot_choice = random.choice(options)
    user_choice = interaction.data['custom_id']
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    result = ""
    
    if user_choice == bot_choice:
        result = ("비겼습니다. 한 판 더 해주세요. \n"
                  f"( {user_nickname} : {user_choice}, 토키 : {bot_choice} )")
        
    elif (user_choice == '가위' and bot_choice == '보') or \
         (user_choice == '바위' and bot_choice == '가위') or \
         (user_choice == '보' and bot_choice == '바위'):
        result = ("제가 졌습니다. \n"
                  "... \n딱히 승부욕을 느낀다거나, 그런 건 아닙니다만. \n"
                  f"( {user_nickname} : {user_choice}, 토키 : {bot_choice} )")
    else: 
        result = ("제가 이겼어요. 얏호~ \n"
                  f"( {user_nickname} : {user_choice}, 토키 : {bot_choice} )")

    await interaction.response.edit_message(content=result, view=None)

# 31


@bot.tree.command(name="31_시작", description="토키와 베스킨라빈스 게임을 시작합니다")
async def thirtyone_start(interaction: discord.Interaction):
    await bot.ThirtyOne.start_game_interaction(interaction)

@bot.tree.command(name="31", description="31 - 숫자를 추측합니다")
async def thirtyone(interaction: discord.Interaction, add: str):
    await bot.ThirtyOne.add_number(interaction, add)

@bot.tree.command(name="31_포기", description="31 - 게임을 포기합니다")
async def thirtyone_giveup(interaction: discord.Interaction):
    await bot.ThirtyOne.give_up(interaction)

# 운세 명령어

@bot.tree.command(name="운세", description="토키가 오늘의 운세를 알려줍니다")
async def 운세(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    user_id = interaction.user.id
    if bot.fortune_manager.can_show_fortune(user_id):
        fortune = bot.fortune_manager.get_random_fortune()
        bot.fortune_manager.set_last_fortune(user_id, fortune)
        bot.fortune_manager.update_last_fortune_date(user_id)
        await interaction.response.send_message(f"[{user_nickname}님의 오늘의 운세]\n"
                                                f"\n{fortune}")
    else:
        last_fortune = bot.fortune_manager.get_last_fortune(user_id)
        if last_fortune:
            await interaction.response.send_message(f"[{user_nickname}님의 오늘의 운세]\n"
                                                    f"\n{last_fortune}")                               
        else:
            await interaction.response.send_message("운세 메시지를 불러올 수 없습니다. 다시 시도해 주세요.")
   
# 기본 명령어

@bot.tree.command(name='안녕', description="토키에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    await interaction.response.send_message(f"앗 {user_nickname}님, 안녕하세요.")

@bot.tree.command(name='청소', description="토키가 청소를 합니다")
async def 청소(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    await interaction.response.send_message(f"쓱싹쓱싹.. {user_nickname}님, 보고 계신가요?")

@bot.tree.command(name='퍽', description="토키를 때립니다")
async def 퍽(interaction: discord.Interaction):
    await interaction.response.send_message("아야..")

@bot.tree.command(name='쓰담', description="토키를 쓰다듬습니다")
async def 쓰담(interaction: discord.Interaction):
    await interaction.response.send_message("엣. . 갑자기요? 저야 좋습니다만.")

@bot.tree.command(name='서브웨이', description="토키가 서브웨이 레시피를 추천해줍니다")
async def 서브웨이(interaction: discord.Interaction):
    await interaction.response.send_message("[메뉴]\n"
                                            "클럽 / 이탈리안 비엠티 + 에그마요 / 쉬림프 + 에그마요 / k바비큐 + 에그마요 \n"
                                            "\n[빵]\n"
                                            "화이트 / 파마산 / 플랫브레드 \n"
                                            "\n[치즈]\n"
                                            "모짜렐라 \n "
                                            "\n[야채]\n"
                                            "알아서 \n "
                                            "\n[소스]\n"
                                            "스위트칠리 + 어니언 / 랜치 + 스위트칠리 / 스위트어니언 + 치폴레 / 스모크바비큐 + 스위트칠리 \n"
                                            "\n[팁]\n"
                                            "소스에 소금/후추를 추가해보세요. \n"
                                            "오븐에 토스팅하기 전에 피망/양파를 추가해서 같이 토스팅해보세요. \n"
                                            "일일이 고르는 게 귀찮으시다면, 내용물이 고정되어있는 썹픽이나 랩을 주문하는 것도 추천드립니다.")

# 봇 실행

async def main():
    async with bot:
        await bot.start(ttoken)

import asyncio
asyncio.run(main())
