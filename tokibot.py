import discord
from discord import app_commands
from discord.ext import tasks
import datetime
from datetime import datetime, time, timedelta
import time
import asyncio


token = "MTI2NzEyNTczMzk2MTEwOTUxNA.GBqLjK.Jpd9QwikmgDKEjQh48jRbAEnS0ioP4WKOZogxg"
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


@tasks.loop(seconds=1)
async def every_write_forum():
    dt = datetime.datetime.now()
    channel = client.get_channel(tchid)
    if (dt.hour == 2) and (dt.minute == 32) and (dt.second > 30):
        await channel.send("test")
        await asyncio.sleep(10)
        
    

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

client.run(token)
