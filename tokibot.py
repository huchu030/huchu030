import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import tracemalloc
import random
import pytz

# 토큰, 채널 ID

TOKEN = 'MTI2NzEyNTczMzk2MTEwOTUxNA.GBqLjK.Jpd9QwikmgDKEjQh48jRbAEnS0ioP4WKOZogxg'
mchid = 1266916147639615639

# 인텐트 설정

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# 운세

class FortuneManager:
    def __init__(self):
        self.user_last_fortune_date = {}  # 유저별 마지막 운세 조회 날짜 저장
        self.user_last_fortune = {}

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

# 봇 클래스 정의

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False
        self.fortune_manager = FortuneManager()
        self.fortunes = [  # 운세 메시지 리스트
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
            "오늘은 서브웨이를 드셔보세요. '/서브웨이' 명령어를 사용해 레시피를 추천받을 수 있습니다."
        ]

    async def on_ready(self):
        print(f'봇이 로그인되었습니다: {self.user.name}')
        if not self.synced:
            await self.tree.sync()
            print("슬래시 명령어가 동기화되었습니다.")
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()

bot = MyBot()

# 알림 메시지

schedule_times_messages = [
    ('00:00', '잘 시간입니다. 좋은 꿈 꾸세요.'),
    ('08:00', '일어날 시간입니다. 아침밥도 드셔야 해요.'),
    ('12:00', '오늘의 점심은, 무엇인가요?'),
    ('16:00', '심심하지 않으신가요? 그럴 땐, 도박을 권장드립니다.'),
    ('22:00', '오늘도 수고하셨습니다. 물론 저도요. 뿅뿅'),
]
tz = pytz.timezone('Asia/Seoul')

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
                    await asyncio.sleep(60)  # Avoid multiple messages within the same minute
                else:
                    print(f'[ERROR] 채널없어')

                break
        else:
            print('[DEBUG] 지정시각아니야')
    except Exception as e:
        print(f'[ERROR] 오류 발생: {e}')

# 가위바위보

@bot.tree.command(name="가위바위보", description="토키와 가위바위보를 합니다")
async def rock_paper_scissors(interaction: discord.Interaction):
    options = ['가위', '바위', '보']

    # 버튼 생성
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
    
    result = ""
    
    if user_choice == bot_choice:
        result = f"비겼습니다. 한 판 더 해주세요. \n( 당신 : {user_choice}, 토키 : {bot_choice} )"
    elif (user_choice == '가위' and bot_choice == '보') or \
         (user_choice == '바위' and bot_choice == '가위') or \
         (user_choice == '보' and bot_choice == '바위'):
        result = f"제가 졌습니다. \n... \n딱히 승부욕을 느낀다거나, 그런 건 아닙니다만. \n( 당신 : {user_choice}, 토키 : {bot_choice} )"
    else: 
        result = f"제가 이겼어요. 얏호~ \n( 당신 : {user_choice}, 토키 : {bot_choice} )"

    await interaction.response.edit_message(content=result, view=None)

# 기본 명령어

@bot.tree.command(name='안녕', description="토키에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("안녕하세요.")

@bot.tree.command(name='청소', description="토키가 청소를 합니다")
async def 청소(interaction: discord.Interaction):
    await interaction.response.send_message("쓱싹쓱싹..")

@bot.tree.command(name='퍽', description="토키를 때립니다")
async def 퍽(interaction: discord.Interaction):
    await interaction.response.send_message("아야..")

@bot.tree.command(name='쓰담', description="토키를 쓰다듬습니다")
async def 쓰담(interaction: discord.Interaction):
    await interaction.response.send_message("엣. . 갑자기요? 저야 좋습니다만.")

@bot.tree.command(name='서브웨이', description="토키가 서브웨이 레시피를 추천해줍니다")
async def 서브웨이(interaction: discord.Interaction):
    await interaction.response.send_message("[메뉴] \n클럽 / 이탈리안 비엠티 + 에그마요 / 쉬림프 + 에그마요 / k바비큐 + 에그마요 \n \n[빵] \n화이트 / 파마산 / 플랫브레드 \n \n[치즈] \n모짜렐라 \n \n[야채] \n알아서 \n \n[소스] \n스위트칠리 + 어니언 / 랜치 + 스위트칠리 / 스위트어니언 + 치폴레 / 스모크바비큐 + 스위트칠리 \n \n[팁] \n소스에 소금/후추를 추가해보세요. \n오븐에 토스팅하기 전에 피망/양파를 추가해서 같이 토스팅해보세요. \n일일히 고르는 게 귀찮으시다면, 내용물이 고정되어있는 썹픽이나 랩을 주문하는 것도 추천드립니다.")

@bot.tree.command(name="운세", description="토키가 오늘의 운세를 알려줍니다")
async def 운세(interaction: discord.Interaction):
    await interaction.response.defer()
    
    user_id = interaction.user.id
    if bot.fortune_manager.can_show_fortune(user_id):
        fortune = random.choice(bot.fortunes)  # 리스트에서 랜덤으로 메시지 선택
        bot.fortune_manager.set_last_fortune(user_id, fortune)
        bot.fortune_manager.update_last_fortune_date(user_id)
        await interaction.response.followup.send(f"{fortune}")
    else:
        last_fortune = bot.fortune_manager.get_last_fortune(user_id)
        if last_fortune:
            await interaction.followup.send(f"{last_fortune}")
        else:
            await interaction.followup.send("운세 메시지를 불러올 수 없습니다. 다시 시도해 주세요.")

# 봇 실행

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
