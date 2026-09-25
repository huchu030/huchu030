import discord
from discord.ext import commands, tasks
from discord import app_commands, ButtonStyle, Interaction, ui
import datetime
from datetime import datetime
import pytz
import tracemalloc
import random
import asyncio
import json
import os
from tokens import jtoken

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# 추가 데이터

data_file = 'add_data.json'
class AddDataManager:

    @staticmethod
    def initialize_data():
        if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
            default_data = {
                "count": 0
            }
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)
            print(f"추가 데이터를 생성했습니다: {data_file}")

    @staticmethod
    def load_data():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            print(f"[ERROR] 추가 데이터 불러오기 오류: {e}")
            return {
                "count": 0
            }

    @staticmethod
    def save_data(data):
        try:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"[ERROR] 추가 데이터 저장 오류: {e}")

# 봇 설정

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
        tracemalloc.start()

bot = MyBot()

@bot.tree.command(name='안녕', description="봇한테 인사를 합니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("안녕하노")

@bot.tree.command(name='니얼굴', description="맞짱신청")
async def 니얼굴(interaction: discord.Interaction):
    await interaction.response.send_message("ㅗ")

@bot.tree.command(name='경제살리기', description="대한민국의 경제발전에 기여합니다")
async def 추가(interaction: discord.Interaction):
    data = AddDataManager.load_data()
    add_count = random.randint(1, 3)
    data["count"] += add_count
    AddDataManager.save_data(data)
    await interaction.response.send_message(f"석유 {add_count}L 발견! \n- 누적 채굴량 : {data['count']}L")

async def main():
    async with bot:
        await bot.start(jtoken)

import asyncio
asyncio.run(main())
