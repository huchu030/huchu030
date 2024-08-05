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

# 토큰, 채널 ID

TOKEN = "MTI2NzEyNDUwNTY4MDI4MTYyMA.Gp_5nb.WpD1gpVbMCVCPrIHIb53jupN67qHj0ps58FE8k"
MCHID = 1266916147639615639 

# 인텐트 설정

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# 숫자야구

class NumberBaseballGame:
    def __init__(self):
        self.reset_game()

    def generate_secret_number(self):
        return ''.join(random.sample('123456789', 3))

    def reset_game(self):
        self.secret_number = None
        self.guesses = []
        self.game_active = False
        self.attempts = 0
        self.max_attempts = 9

    def start_game(self):
        self.secret_number = self.generate_secret_number()
        self.guesses = []
        self.game_active = True
        self.attempts = 0

    def make_guess(self, guess):
        if len(guess) != 3 or len(set(guess)) != 3 or not guess.isdigit():
            return "3자리의 서로 다른 숫자를 입력해야 합니다!"
        guess_list = list(map(int, guess))
        self.guesses.append(guess)
        self.attempts += 1

        if guess == self.secret_number:
            self.game_active = False
            return f"와아~ 정답이에요! 답은 {self.secret_number}! \n{self.attempts}회 만에 맞혔어요~"

        if self.attempts >= self.max_attempts:
            self.game_active = False
            return (f"{guess} : 기회를 모두 소진했어요. 끄앙 \n"
                    f"정답은 {self.secret_number}입니다! 다시 도전해 볼까요?")

        strikes, balls = self.calculate_strikes_and_balls(guess)
        return f"{guess} : {strikes}S {balls}B"
    
    def calculate_strikes_and_balls(self, guess):
        strikes = sum(1 for a, b in zip(guess, self.secret_number) if a == b)
        balls = sum(1 for g in guess if g in self.secret_number) - strikes
        return strikes, balls

class NumberBaseball:
    def __init__(self):
        self.games = {}

    def get_game(self, user):
        if user.id not in self.games:
            self.games[user.id] = NumberBaseballGame()
        return self.games[user.id]

    async def start_game_interaction(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if game.game_active:
            await interaction.response.send_message("저와 이미 게임을 하고 있어요!")
        else:
            game.start_game()
            await interaction.response.send_message("뽜밤뽜밤-! 숫자야구 게임을 시작합니다! \n"
                                                    "`/숫자야구_추측`으로 3자리 숫자를 맞혀보세요. \n"
                                                    "`/숫자야구_규칙`으로 게임 규칙을 볼 수 있습니다!")

    async def guess_number(self, interaction: discord.Interaction, guess: str):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
        else:
            result = game.make_guess(guess)
            await interaction.response.send_message(result)

    async def give_up(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기도 하는 법!")
        else:
            game.game_active = False
            await interaction.response.send_message(f"게임을 포기했습니다. 정답은 {game.secret_number}입니다! \n"
                                                    "아리스랑 놀아주세요...")
# 숫자게임

class NumberGuessingGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.secret_number = None
        self.attempts = 0
        self.game_active = False

    def start_game(self, min_number=1, max_number=100):
        self.secret_number = random.randint(min_number, max_number)
        self.attempts = 0
        self.game_active = True

    def make_guess(self, guess):
        self.attempts += 1
        guess = int(guess)
        if guess < self.secret_number:
            return f"{guess} : 더 높아요!"
        elif guess > self.secret_number:
            return f"{guess} : 더 낮아요!"
        else:
            self.game_active = False
            return (f"와아~ 정답이에요! 답은 {self.secret_number}! \n"
                    f"{self.attempts}회 만에 맞혔어요~")

class NumberGuessing:
    def __init__(self):
        self.games = {} 

    def get_game(self, user):
        if user.id not in self.games:
            self.games[user.id] = NumberGuessingGame()
        return self.games[user.id]

    async def start_game_interaction(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if game.game_active:
            await interaction.response.send_message("저와 이미 게임을 하고 있어요!")
        else:
            game.start_game()
            await interaction.response.send_message("뽜밤뽜밤-! 숫자 맞히기 게임을 시작합니다! \n"
                                                    "`/숫자게임_추측`으로 1부터 100까지의 숫자를 맞혀보세요.")

    async def guess_number(self, interaction: discord.Interaction, guess: str):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
        else:
            if not guess.isdigit() or not (1 <= int(guess) <= 100):
                await interaction.response.send_message("1부터 100까지의 숫자만 입력해주세요!")
                return
            
            result = game.make_guess(guess)
            await interaction.response.send_message(result)

    async def give_up(self, interaction: discord.Interaction):
        user = interaction.user
        game = self.get_game(user)
        if not game.game_active:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 도전부터 해야 포기도 하는 법!")
        else:
            game.game_active = False
            await interaction.response.send_message(f"게임을 포기했습니다. 정답은 {game.secret_number}입니다! \n"
                                                    "아리스랑 놀아주세요...")
# RPG 게임

data_file = 'game_data.json'

class rpg:

    def __init__(self):
        self.initialize_game_data()

    def initialize_game_data(self):
        if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
            default_data = {
                "players": {},
                "current_enemies": {}
            }
            with open(data_file, 'w') as f:
                json.dump(default_data, f, indent=4)

    def load_game_data(self):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Error loading game data: {e}")
            return {"players": {}, "current_enemies": {}}

    def save_game_data(self, data):
        try:
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Error saving game data: {e}")

    def add_new_player(self, user_id):
        data = self.load_game_data()

        print(f"[DEBUG] Loaded data: {data}")

        if user_id not in data["players"]:

            print(f"[DEBUG] Adding new player with ID {user_id}")
            
            data["players"][user_id] = {
                "level": 1,
                "hp": 100,
                "exp": 0,
                "attack": 0,
                "defense": 0,
                "evasion_chance": 0,
                "attack_chance": 0,
                "critical_chance": 0,
                "critical_damage": 0.5,
                "coins": 0,
                "evasion_items": 0
            }
            data["current_enemies"][user_id] = {
                "hp": 50
            }

            print(f"[DEBUG] Saving data: {data}")
            
            self.save_game_data(data)
        else:
            print(f"[DEBUG] Player with ID {user_id} already exists.")

    def is_player_in_game(self, user_id):
        data = self.load_game_data()
        return user_id in data["players"]
            
    def delete_player_data(self, user_id):
        data = self.load_game_data()
        if user_id in data["players"]:
            del data["players"][user_id]
            del data["current_enemies"][user_id]
            self.save_game_data(data)
            
    async def start_game(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if self.is_player_in_game(user_id):
            await interaction.response.send_message("`/공격`으로 빨리 적을 공격하세요!")
        else:
            self.add_new_player(user_id)
            await interaction.response.send_message("용사여. 빛이 당신과 함께 합니다...\n"
                                                    "`/rpg_규칙`으로 게임 규칙을 볼 수 있습니다.\n"
                                                    "앗, 방심한 사이에 쨈미몬이 나타났습니다. 어서 공격하세요!")
        
    async def attack(self, interaction: discord.Interaction, damage: str):
        data = self.load_game_data()
        guild = interaction.guild
        user_nickname = get_user_nickname(guild, interaction.user.id)
        user_id = str(interaction.user.id)

        if user_id not in data["players"]:
            await interaction.response.send_message("진행 중인 게임이 없습니다. 아리스랑 같이 놀아요!")
            return
        
        player = data["players"][user_id]
        enemy = data["current_enemies"][user_id]
        
        if not damage.isdigit() or not (1 <= int(damage) <= player["hp"]):
            await interaction.response.send_message("체력 이하의 숫자를 입력해주세요! \n"
                                                    "`/스탯`으로 현재 체력을 확인할 수 있습니다.")
            return

        damage = int(damage)

        success_chance = random.randint(0, 90) + player["attck_chance"]
        actual_chance = random.randint(0, 90)
        attack_success = actual_chance <= success_chance
        
        critical_hit = random.randint(1, 100) <= player["critical_chance"]
        total_damage = damage + player["attack"]

        if attack_success:

            if critical_hit:
                critical_bonus = damage * player["critical_damage"]
                total_damage += round(critical_bonus)
                result = "\n크리티컬!!!!!"
                
            enemy["hp"] -= total_damage
            result = (f"\n공격 성공! 쨈미몬이 {damage}의 데미지를 입었습니다. ( 성공 확률 : {success_chance}% )\n"
                      "( 쨈미몬 : 으앙 )\n"
                      f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}")

            if enemy["hp"] <= 0:
                exp_gain = random.randint(30, 40)
                coin_gain = random.randint(10, 20)
                player["exp"] += exp_gain
                player["coins"] += coin_gain
                result += ("\n\n와아~ 쨈미몬이 쓰러졌습니다.\n"
                           f"경험치 {exp_gain}, 코인 {coin_gain} 획득!")

                if player["exp"] >= player["level"] * 100:
                    player["hp"] = 100
                    player["level"] += 1
                    enemy["hp"] = 40 + 10 * player["level"]

                    stat_to_increase = random.choice(["attack", "defense", "evasion_chance", "critical_chance"])
                    if stat_to_increase == "attack":
                        player["attack"] += 1
                    elif stat_to_increase == "defense":
                        player["defense"] += 1
                    elif stat_to_increase == "evasion_chance":
                        player["evasion_chance"] += 1
                    elif stat_to_increase == "critical_chance":
                        player["critical_chance"] += 1
                    
                    result += (f"\n \n레벨 업! 현재 레벨 : {player['level']}"
                               "...\n"
                               "헉.. 쨈미몬이 더 강해져서 돌아왔어요! 끄앙\n"
                               f"현재 쨈미몬의 체력 : {enemy['hp']}")
                else:
                    player["hp"] = 100
                    enemy["hp"] = 40 + 10 * player["level"]
                    result += ("\n...\n" 
                               "헉.. 쨈미몬이 다시 깨어났어요!\n"
                               f"현재 쨈미몬의 체력 : {enemy['hp']}")      
        else:
            evasion = random.randint(1, 100) <= player["evasion_chance"]
            
            if player["evasion_items"] > 0:
                player["evasion_items"] -= 1
                result = (f"공격 실패! 쨈미몬이 반격해 {actual_damage}의 데미지를 입힐..뻔 했지만\n"
                          f"{user_nickname}님이 어제 산 '수학의 정석'이 공격을 막아주었습니다! ( 성공 확률 : {success_chance}% )\n"
                          f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}\n"
                          f"남은 수학의 정석 : {player['evasion_items']}개")
            elif evasion:
                result = (f"공격 실패! 쨈미몬이 반격해 {actual_damage}의 데미지를 입힐..뻔 했지만 회피했습니다! 럭키~\n"
                          f"( 성공 확률 : {success_chance}%, 회피 확률 : {player['evasion']}% )\n"
                          f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}")
            else:
                actual_damage = max(10, damage - player["defense"])
                player["hp"] -= actual_damage
                result = (f"공격 실패! 쨈미몬이 반격해 {actual_damage}의 데미지를 입혔습니다. ( 성공 확률 : {success_chance}% )\n"
                            f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}")
                if player["hp"] <= 0:
                    result += f"\n \n{user_nickname}님의 체력이 0이 되어 사망했습니다. 끄앙"
                    self.delete_player_data(user_id)
                    await interaction.response.send_message(result)
                    return
        
        self.save_game_data(data)
        await interaction.response.send_message(result)

    async def stats(self, interaction: discord.Interaction):
        print(f"[DEBUG] Interaction data: {interaction.data}")
        data = self.load_game_data()
        guild = interaction.guild
        user_nickname = get_user_nickname(guild, interaction.user.id)
        user_id = str(interaction.user.id)

        player_data = data.get("players", {}).get(user_id, None)
        enemy_data = data.get("current_enemies", {}).get(user_id, None)
        
        if player_data:
            print(f"[DEBUG] player_data: {player_data}")
            try:
                await interaction.response.send_message(f"[{user_nickname}님의 스탯] \n"
                                                        f"\n레벨 : {player_data['level']}, 체력 : {player_data['hp']}, 경험치 : {player_data['exp']}\n"
                                                        f"공격력 : {player_data['attack']}, 방어력 : {player_data['defense']}\n"
                                                        f"회피 확률 : {player_data['evasion_chance']}%, 공격 성공 확률 : + {player_data['attack_chance']}%p\n"
                                                        f"크리티컬 확률 : {player_data['critical_chance']}%, 크리티컬 데미지 : {player_data['critical_damage']*100}%\n"
                                                        f"수학의 정석 : {player_data['evasion_items']}개\n"
                                                        f"코인 : {player_data['coins']}\n"
                                                        f"\n현재 쨈미몬의 체력 : {enemy_data['hp']}")
            except discord.errors.Forbidden:
                print("[ERROR] 메시지를 보낼 수 없습니다. 봇의 권한을 확인해주세요.")
            except Exception as e:
                print(f"[ERROR] 오류 발생: {e}")
        else:
            await interaction.response.send_message(f"{user_nickname}님의 데이터가 없습니다. `/rpg`로 게임을 시작해보세요!")

    async def leaderboard(self, interaction: discord.Interaction):
        guild = interaction.guild
        user_nickname = get_user_nickname(guild, interaction.user.id)
        data = self.load_game_data()
        sorted_players = sorted(
            [(user_id, player) for user_id, player in data["players"].items()],
            key=lambda x: x[1]["exp"], reverse=True)

        leaderboard_message = "RPG 게임 순위:\n"
        for rank, (user_id, player) in enumerate(sorted_players, start=1):
            user_nickname = get_user_nickname(guild, int(user_id))
            leaderboard_message += f"{rank}. {user_nickname} - 레벨: {player['level']}, 경험치: {player['exp']}, 코인: {player['coins']}\n"

        await interaction.response.send_message(leaderboard_message)


class Shop(ui.View):
    ITEMS = {
        "shop_attack": {"label": "버섯", "price": 100, "effect": "attack"},
        "shop_defense": {"label": "고양이", "price": 100, "effect": "defense"},
        "shop_evasion_chance": {"label": "네잎클로버", "price": 150, "effect": "evasion_chance"},
        "shop_attack_chance": {"label": "헬스장 월간이용권", "price": 150, "effect": "attack_chance"},
        "shop_critical_chance": {"label": "안경", "price": 150, "effect": "critical_chance"},
        "shop_critical_damage": {"label": "민트초코", "price": 150, "effect": "shop_critical_damage"},
        "shop_evasion_items":  {"label": "수학의 정석", "price": 200, "effect": "shop_evasion_items"}
    }
    
    def __init__(self, user_id, rpg_game):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.rpg_game = rpg_game
        for item_id, item_info in self.ITEMS.items():
            custom_id = f"shop_{item_id}"
            self.add_item(ui.Button(label=f"{item_info['label']}", style=discord.ButtonStyle.primary, custom_id=item_id))

    @ui.button(label="버섯", style=discord.ButtonStyle.primary, custom_id="shop_attack")
    async def shop_attack(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_attack")

    @ui.button(label="고양이", style=discord.ButtonStyle.primary, custom_id="shop_defense")
    async def shop_defense(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_defense")

    @ui.button(label="네잎클로버", style=discord.ButtonStyle.primary, custom_id="shop_evasion_chance")
    async def shop_evasion_chance(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_evasion_chance")

    @ui.button(label="헬스장 월간이용권", style=discord.ButtonStyle.primary, custom_id="shop_attack_chance")
    async def shop_attack_chance(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_attack_chance")

    @ui.button(label="안경", style=discord.ButtonStyle.primary, custom_id="shop_critical_chance")
    async def shop_critical_chance(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_critical_chance")

    @ui.button(label="민트초코", style=discord.ButtonStyle.primary, custom_id="shop_critical_damage")
    async def shop_critical_damage(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_critical_damage")

    @ui.button(label="수학의 정석", style=discord.ButtonStyle.primary, custom_id="shop_evasion_items")
    async def shop_evasion_items(self, interaction: discord.Interaction, button: ui.Button):
        await self.purchase_item(interaction, "shop_evasion_items")


    async def purchase_item(self, interaction: discord.Interaction, item_id: str):
        try:
            data = await self.rpg_game.load_game_data()
            user_id = str(interaction.user.id)
            guild = interaction.guild
            user_nickname = get_user_nickname(guild, interaction.user.id)
            player_data = data["players"].get(user_id)
        
            if user_id not in data["players"]:
                await interaction.response.send_message("코인이 없습니다. `/rpg`로 게임을 시작해보세요!", ephemeral=False)
                return

            item_info = self.ITEMS.get(item_id)
            if not item_info:
                await interaction.response.send_message("[ERROR] 아이템이 품절되었습니다.", ephemeral=False)
                return
    
            if player_data["coins"] < item_info['price']:
                await interaction.response.send_message(f"코인이 부족합니다! 현재 코인: {player['coins']}", ephemeral=False)
                return

            player_data["coins"] -= item_info['price']
            result = ""

            if item_info["effect"] == "attack":
                player["attack"] += 1
                result = "공격력이 1 증가했습니다!"
                      
            elif item_info["effect"] == "defense":
                player["defense"] += 1
                result = "방어력이 1 증가했습니다!"
            
            elif item_info["effect"] == "evasion_chance":
                player["evasion_chance"] += 1
                result = "회피 확률이 1%p 증가했습니다!"
            
            elif item_info["effect"] == "attack_chance":
                player["attack_chance"] += 1
                result = "공격 확률이 1%p 1 증가했습니다!"
            
            elif item_info["effect"] == "critical_chance":
                player["critical_chance"] += 1
                result = "크리티컬 확률이 1%p 증가했습니다!"
            
            elif item_info["effect"] == "critical_damage":
                player["critical_damage"] += 1
                result = "크리티컬 데미지가 5%p 증가했습니다!"
            
            elif item_info["effect"] == "evasion_items":
                player["evasion_items"] += 1
                result = f"수학의 정석이 {player_data['evasion_items']}개가 되었습니다!"

            result += f"\n`/스탯`으로 {user_nickname}님의 현재 능력치를 확인해보세요~"

            await self.rpg_game.save_game_data(data)
            await interaction.response.send_message(result, ephemeral=False)
            
        except Exception as e:
            print(f"[ERROR] Error in purchase_item: {e}")
            await interaction.response.send_message("[ERROR] 상점 알바가 화장실에 갔습니다. 사장님에게 문의해주세요", ephemeral=True)

# 봇 설정

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', intents=intents, **kwargs)
        self.synced = False
        self.number_baseball = NumberBaseball()
        self.number_guessing = NumberGuessing()
        self.rpg = rpg()
        
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

# 환영 메시지

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(MCHID)
    if channel:
        await channel.send('인간이 이곳에 온 것은 수천 년 만이군...')
    else:
        print('[ERROR] 채널을 찾을 수 없습니다.')

# 알림 메시지

schedule_times_messages = [
    ('19:00', '아리스랑 놀아주세요!')
    ]
lock = asyncio.Lock()
tz = pytz.timezone('Asia/Seoul')

@tasks.loop(hours=1)
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

@bot.tree.command(name="가위바위보", description="아리스와 가위바위보를 합니다")
async def rock_paper_scissors(interaction: discord.Interaction):
    options = ['가위', '바위', '보']
    view = discord.ui.View()
    for option in options:
        button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)
        button.callback = lambda i: button_callback(i, interaction.user)
        view.add_item(button)
        
    await interaction.response.send_message("안 내면 집니다!", view=view)

async def button_callback(interaction: discord.Interaction, user: discord.User):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    
    options = ['가위', '바위', '보']
    bot_choice = random.choice(options)
    user_choice = interaction.data['custom_id']
    result = ""
    
    if user_choice == bot_choice:
        result = ("비겼습니다. 한 판 더 해요! \n"
                  f"( {user_nickname} : {user_choice}, 아리스 : {bot_choice} )")
        
    elif (user_choice == '가위' and bot_choice == '보') or \
         (user_choice == '바위' and bot_choice == '가위') or \
         (user_choice == '보' and bot_choice == '바위'):
        result = ("아리스가 졌어요. 끄앙 \n"
                  f"( {user_nickname} : {user_choice}, 아리스 : {bot_choice} )")
        
    else: 
        result = ("아리스가 이겼습니다!! \n"
                  f"( {user_nickname} : {user_choice}, 아리스 : {bot_choice} )")

    await interaction.response.edit_message(content=result, view=None)

# 숫자야구 명령어

@bot.tree.command(name='숫자야구_규칙', description="아리스가 숫자야구의 규칙을 설명해줍니다")
async def 숫자야구_규칙(interaction: discord.Interaction):
    await interaction.response.send_message(
        "[숫자야구 룰]\n"
        "\n아리스가 정한 3자리 숫자를 맞히는 게임입니다!\n"
        "숫자는 0부터 9까지의 서로 다른 숫자 3개이며\n"
        "숫자와 위치가 전부 맞으면 S (스트라이크),\n"
        "숫자와 위치가 틀리면 B (볼) 입니다. \n"
        "\n예시를 들어볼까요? 제가 정한 숫자가 ‘123’이면\n"
        "456 : 0S 0B\n"
        "781 : 0S 1B\n"
        "130 : 1S 1B\n"
        "132 : 1S 2B\n"
        "123 : 3S 0B 입니다! \n"
        "\n아리스랑 같이 놀아요 끄앙")

@bot.tree.command(name="숫자야구", description="아리스와 숫자야구 게임을 시작합니다")
async def 숫자야구(interaction: discord.Interaction):
    await bot.number_baseball.start_game_interaction(interaction)

@bot.tree.command(name="숫자야구_추측", description="숫자야구 - 숫자를 추측합니다")
async def 숫자야구_추측(interaction: discord.Interaction, guess: str):
    await bot.number_baseball.guess_number(interaction, guess)

@bot.tree.command(name="숫자야구_포기", description="숫자야구 - 게임을 포기합니다")
async def 숫자야구_포기(interaction: discord.Interaction):
    await bot.number_baseball.give_up(interaction)

# 숫자게임 명령어

@bot.tree.command(name="숫자게임", description="아리스와 숫자 맞히기 게임을 시작합니다")
async def 숫자추측(interaction: discord.Interaction):
    await bot.number_guessing.start_game_interaction(interaction)

@bot.tree.command(name="숫자게임_추측", description="숫자게임 - 숫자를 추측합니다")
async def 숫자추측_추측(interaction: discord.Interaction, guess: str):
    await bot.number_guessing.guess_number(interaction, guess)

@bot.tree.command(name="숫자게임_포기", description="숫자게임 - 게임을 포기합니다")
async def 숫자추측_포기(interaction: discord.Interaction):
    await bot.number_guessing.give_up(interaction)

# RPG게임 명령어

@bot.tree.command(name="rpg", description="아리스와 RPG 게임을 시작합니다")
async def rpg(interaction: discord.Interaction):
    await bot.rpg.start_game(interaction)

@bot.tree.command(name="공격", description="rpg - 적을 공격합니다")
async def 공격(interaction: discord.Interaction, damage: str):
    await bot.rpg.attack(interaction, damage)

@bot.tree.command(name="스탯", description="rpg - 자신의 스탯을 확인합니다")
async def 스탯(interaction: discord.Interaction):
    await bot.rpg.stats(interaction)

@bot.tree.command(name="순위", description="rpg - 유저들의 순위를 확인합니다")
async def 순위(interaction: discord.Interaction):
    await bot.rpg.leaderboard(interaction)

@bot.tree.command(name="상점", description="rpg - 상점으로 들어갑니다")
async def 상점(interaction: discord.Interaction):
    try:
        user_id = str(interaction.user.id)
        shop_view = Shop(user_id=user_id, rpg_game=bot.rpg)
        await interaction.response.send_message("상점에 오신 것을 환영합니다! 다음 아이템을 구매할 수 있습니다\n"
                                                "\n1. 버섯 : 쨈미몬이 싫어합니다. 공격력이 증가합니다. ( 100 coins )\n"
                                                "2. 고양이 : 쨈미몬이 좋아합니다. 방어력이 증가합니다. ( 100 coins )\n"
                                                "3. 네잎클로버 : 행운을 불러옵니다. 회피 확률이 증가합니다. ( 100 coins )\n"
                                                "4. 안경 : 시력이 상승합니다. 크리티컬 확률이 증가합니다. ( 150 coins )\n"
                                                "5. 민트초코 : 쨈미몬이 극혐합니다. 크리티컬 데미지가 증가합니다. ( 150 coins )\n"
                                                "6. 수학의 정석 : 책이 공격을 대신 받아줍니다. 찢어지면 다시 쓸 수 없으며, 여러 개 구매할 수 있습니다. ( 200 coins )\n"
                                                , view=shop_view)
    except Exception as e:
        print(f"[ERROR] Error in 상점 command: {type(e)}, {e}")
        await interaction.response.send_message("[ERROR] 상점이 폐업했습니다. 쟌넨" , ephemeral=False)


@bot.tree.command(name='rpg_규칙', description="아리스가 RPG게임의 규칙을 설명해줍니다")
async def rpg_규칙(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    await interaction.response.send_message(
        f"{user_nickname}님은 사악한 어둠의 쨈미몬을 물리치기 위해 모험을 떠난 용사입니다!\n"
        "\n[공격 방식]\n"
        f"\n`/공격`으로 {user_nickname}님의 체력 이하의 숫자를 입력하면 공격을 시도할 수 있습니다.\n"
        f"\n{user_nickname}님의 체력은 100, 쨈미몬의 체력은 50으로 시작합니다. \n"
        "공격은 랜덤한 확률로 성공하며, 성공시 쨈미몬에게 입력한 숫자만큼의 데미지를 입힙니다.\n"
        f"그러나 실패시 쨈미몬이 반격해 {user_nickname}님이 그만큼의 데미지를 입습니다!\n"
        "\n[레벨업]\n"
        "쨈미몬을 쓰러뜨릴 때마다 체력이 회복되고 코인을 얻습니다.\n"
        "또한 랜덤한 경험치가 쌓이며 경험치가 100단위를 넘기면 레벨업을 합니다.\n"
        f"레벨이 올라갈 때마다 쨈미몬이 강해지며, {user_nickname}님의 스탯 중 랜덤으로 하나가 상승합니다.\n"
        "\n체력이 0이 되면 사망하여 게임이 초기화되니 부디 조심하세요!\n"
        "`/상점`에서 코인으로 여러 아이템들을 구매하실 수 있으니 들러보시길 바랍니다.\n"
        "그럼 저는 이만...")
        
# 로또                                                     

@bot.tree.command(name="로또", description="아리스가 로또 번호를 골라줍니다")
async def 로또(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    await interaction.response.send_message(f"{user_nickname}님의 이번 주 로또 번호는~ \n"
                                            f"[ {', '.join(map(str, numbers))} ] 입니다! 당첨되면 저도...")
# 기본 명령어

@bot.tree.command(name='안녕', description="아리스에게 인사를 건넵니다")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("뽜밤뽜밤-!")

@bot.tree.command(name='로봇주제에', description="아리스를 놀립니다")
async def 로봇주제에(interaction: discord.Interaction):
    await interaction.response.send_message("아리스는 로봇이 아닙니다!!")

@bot.tree.command(name='밥', description="아리스에게 밥을 줍니다")
async def 밥(interaction: discord.Interaction):
    await interaction.response.send_message("응..? 아리스는 건전지를 먹지 않습니다!")

@bot.tree.command(name='쓰담', description="아리스의 인공 단백질 피부가 따뜻해집니다")
async def 쓰담(interaction: discord.Interaction):
    guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)
    await interaction.response.send_message(f"{user_nickname}님, 아리스는 행복합니다..")

# 봇 실행

async def main():
    async with bot:
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
