import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio


token = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
intents = discord.Intents.all()

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

client = aclient()
tree = app_commands.CommandTree(client)

mchid = 1266916147639615639
tchid = 1267153846258499675

    

@tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!", ephemeral=False)
    

@tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!", ephemeral=False)


@tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 건전지를 먹지 않습니다!!", ephemeral=False)


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
