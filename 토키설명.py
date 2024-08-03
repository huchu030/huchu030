import discord
from discord.ext import commands, tasks
import datetime
from datetime import datetime
import asyncio
import tracemalloc
import random
import pytz



# 운세

class FortuneManager:
    def __init__(self):
        self.user_last_fortune_date = {}
        self.user_last_fortune = {}
        self.fortunes = [
            "오늘은 행운이 가득한 날입니다.",
            "조금 더 노력하면 큰 성과를 얻을 수 있을 것입니다.",
            "누군가가 당신에게 도움을 줄 것입니다.",
            "오늘은 도전 정신이 필요한 날입니다. 어려운 문제를 해결하는 기회로 삼으세요."
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

# 봇

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False
        self.fortune_manager = FortuneManager()
        
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
    ('16:00', "심심하지 않으신가요? 그럴 땐, `/도박`을 권장드립니다."),
    ('22:00', '오늘도 수고하셨습니다. 물론 저도요. 뿅뿅')
    ]



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
        await interaction.response.send_message(f"[오늘의 {user_nickname}님의 운세]\n"
                                                f"\n{fortune}")
    else:
        last_fortune = bot.fortune_manager.get_last_fortune(user_id)
        if last_fortune:
            await interaction.response.send_message(f"[{user_nickname}님의 오늘의 운세]\n"
                                                    f"\n{last_fortune}")                               
        else:
            await interaction.response.send_message("운세 메시지를 불러올 수 없습니다. 다시 시도해 주세요.")
