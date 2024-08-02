import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import asyncio
import pytz

# Token and channel IDs
TOKEN = 'MTI2NzEyNTczMzk2MTEwOTUxNA.GBqLjK.Jpd9QwikmgDKEjQh48jRbAEnS0ioP4WKOZogxg'
mchid = 1266916147639615639

# Timezone and intents
tz = pytz.timezone('Asia/Seoul')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# Custom bot class
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False

    async def on_ready(self):
        print(f'봇이 로그인되었습니다: {self.user.name}')
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        scheduled_task.start()
        tracemalloc.start()

# Create bot instance
bot = MyBot()

# Scheduled tasks
schedule_times_messages = [
    ('00:00', '잘 시간입니다. 좋은 꿈 꾸세요.'),
    ('08:00', '일어날 시간입니다. 아침밥도 드셔야 해요.'),
    ('12:00', '오늘의 점심은, 무엇인가요?'),
    ('16:00', '심심하지 않으신가요? 그럴 땐, 도박을 권장드립니다.'),
    ('22:00', '오늘도 수고하셨습니다. 물론 저도요. 뿅뿅'),
]

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

# Slash commands
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


# Run the bot

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
