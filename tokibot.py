import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import time
import asyncio
import logging



token = 'MTI2NzEyNTczMzk2MTEwOTUxNA.GBqLjK.Jpd9QwikmgDKEjQh48jRbAEnS0ioP4WKOZogxg'
tchid = 1267153846258499675
mchid = 1266916147639615639

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(leverlname)s - %(message)s',
    handlers=[
        logging.StreamHandler()])

    
intents = discord.Intents.all()
intents.message_content = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


schedule_times_messages = [
    ('00:00', '잘 시간입니다. 좋은 꿈 꾸세요.'),
    ('08:00', '일어날 시간입니다. 아침밥도 드셔야 해요.'),
    ('12:00', '점심 시간입니다.'),
    ('16:00', '심심하지 않으세요? 도박을 권장드립니다.'),
    ('19:00', '저녁 드실 시간이에요.'),
    ('23:45', '테스트')]


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    scheduled_task.start()



@tasks.loop(seconds=10)
async def scheduled_task():
    try:
        now = datetime.datetime.now()
        current_time = now.time()
        print(f'[DEBUG] 현재시각:{current_time}')
        
        for time_str, message in schedule_times_messages:
            target_time = datetime.datetime.strptime(time_str, '%H:%M').time()
            print(f'[DEBUG] 설정시각:{target_time}')
            
            if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
                print('[DEBUG] 지정시각이당')
                channel = client.get_channel(tchid)
                
                if channel:
                    await channel.send(message)
                    print(f'[DEBUG] 성공')
                else:
                    print(f'[ERROR] 채널없어')
                    
                await asyncio.sleep(60)
                break
        else:
            print('[DEBUG] 지정시각아니야')
            await asyncio.sleep(10)
    except Exception as e:
        print(f'[ERROR] 오류 발생: {e}')


    

@tree.command(name='안녕', description="토키에게 인사를 건넵니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("안녕하세요.", ephemeral=False)

@tree.command(name='청소', description="토키가 청소를 합니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("쓱싹쓱싹..", ephemeral=False)

@tree.command(name='퍽', description="토키를 때립니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("아야..", ephemeral=False)

@tree.command(name='쓰담', description="토키를 쓰다듬습니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("엣. . 갑자기요?", ephemeral=False)

@tree.command(name='테스트', description="테스트입니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("테스트메시지", ephemeral=False)





    

client.run(token)
