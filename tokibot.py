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
    await interaction.response.send_message("안녕하세요.", ephemeral=False)

@bot.tree.command(name='청소', description="토키가 청소를 합니다")
async def 청소(interaction: discord.Interaction):
    await interaction.response.send_message("쓱싹쓱싹..", ephemeral=False)

@bot.tree.command(name='퍽', description="토키를 때립니다")
async def 퍽(interaction: discord.Interaction):
    await interaction.response.send_message("아야..", ephemeral=False)

@bot.tree.command(name='쓰담', description="토키를 쓰다듬습니다")
async def 쓰담(interaction: discord.Interaction):
    await interaction.response.send_message("엣. . 갑자기요? 저야 좋습니다만.", ephemeral=False)


# 봇 실행

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
