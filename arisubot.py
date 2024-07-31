import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import time
import random
import asyncio
import pytz


token = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
tchid = 1267153846258499675
mchid = 1266916147639615639


tz = pytz.timezone('Asia/Seoul')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True



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
    ('19:00', '아리스랑 놀아주세요!'),]


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    scheduled_task.start()

@client.event
async def on_member_join(member):
    channel = client.get_channel(mchid)
    if channel:
        await channel.send('인간이 이곳에 온 것은 수천 년 만이군...')
    else:
        print('...')

@tasks.loop(minutes=1)
async def scheduled_task():
    try:
        now = datetime.datetime.now(tz)
        current_time = now.strftime('%H:%M')
        print(f'[DEBUG] 현재시각:{current_time}')
        
        for time_str, message in schedule_times_messages:
            if current_time == time_str:
                print('[DEBUG] 지정시각이당')
                channel = client.get_channel(mchid)
                
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


    




@tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!", ephemeral=False)
    

@tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!", ephemeral=False)


@tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("응..? 아리스는 건전지를 먹지 않습니다!", ephemeral=False)


class NumberBaseballBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        
    @tree.command(name='숫자야구', description="아리스와 숫자야구 게임을 합니다.")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("게임이 이미 진행 중입니다.")
            return
        self.games[interaction.channel.id] = {
            'number': self.generate_number(),
            'attempts': 0}
        await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임이 시작되었습니다! '/추측'을 사용해, 3자리 숫자를 맞춰보세요~")

    @tree.command(name='추측', description="숫자를 추측합니다.")
    async def guess_number(self, interaction: discord.Interaction, guess: str):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("게임 진행 중이 아닙니다. /숫자야구 명령어로 게임을 시작해보세요!")
            return
        if len(guess) != 3 or not guess.isdigit():
            await interaction.response.send_message("3자리 숫자를 입력하세요.")
            return
        result = self.check_guess(self.games[interaction.channel.id]['number'], guess)
        self.games[interaction.channel.id]['attempts'] += 1

        if result == "3A0B":
            await interaction.response.send_message(f"와아~ 정답입니다! {self.games[interaction.channel.id]['attempts']}회 만에 맞췄어요!")
            del self.games[interaction.channel.id]
        else:
            await interaction.response.send_message(result)
            
    def generate_number(self):
        while True:
            number = ''.join(random.sample('123456789', 3))
            if len(set(number)) == 3:
                return number
    def check_guess(self, number, guess):
        a = sum(n == g for n, g in zip(number, guess))
        b = sum(min(number.count(d), guess.count(d)) for d in set(guess)) - a
        return f"{a}A{b}B"

    

    
        
       
           

        






@tree.command(name='가위바위보', description="아리스와 가위바위보를 합니다")
@app_commands.choices(choices=[
    app_commands.Choice(name="가위", value="가위"),
    app_commands.Choice(name="바위", value="바위"),
    app_commands.Choice(name="보", value="보")])
async def slash3(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    ranNum = (random.randint(1,3))
    if(choices.value == '가위'):
        if ranNum == 1:
            await interaction.response.send_message("(가위) 비겼습니다. 한 판 더!")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 아리스가 이겼습니다!!")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 아리스가 졌어요. 끄앙")
    elif(choices.value == '바위'):
        if ranNum == 1:
            await interaction.response.send_message("(가위) 아리스가 졌어요. 끄앙")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 비겼습니다. 한 판 더!")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 아리스가 이겼습니다!!")
    elif(choices.value == '보'):
        if ranNum == 1:
            await interaction.response.send_message("(가위) 아리스가 이겼습니다!!")
        elif ranNum == 2:
            await interaction.response.send_message("(바위) 아리스가 졌어요. 끄앙")
        elif ranNum == 3:
            await interaction.response.send_message("(보) 비겼습니다. 한 판 더!")



client.run(token)
