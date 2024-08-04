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
        if user_id not in data["players"]:
            data["players"][user_id] = {
                "level": 1,
                "hp": 100,
                "exp": 0,

                # 스탯 추가
                "attack": 10,
                "defense": 5,
                "evasion": 10,
                "critical": 10,
                "coins": 0
            }
            data["current_enemies"][user_id] = {
                "hp": 50
            }
            self.save_game_data(data)

    def delete_player_data(self, user_id):
        data = self.load_game_data()
        if user_id in data["players"]:
            del data["players"][user_id]
            del data["current_enemies"][user_id]
            self.save_game_data(data)

    def is_player_in_game(self, user_id):
        data = self.load_game_data()
        return user_id in data["players"]

    def calculate_next_level_exp(self, level):
        return level * 100

    async def start_game(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        if self.is_player_in_game(user_id):
            await interaction.response.send_message("`/공격`으로 빨리 적을 공격하세요!")
            return

        self.add_new_player(user_id)
        await interaction.response.send_message("용사여. 빛이 당신과 함께 합니다...\n"
                                                "`/rpg_규칙`으로 게임 규칙을 볼 수 있습니다.\n"
                                                "앗, 방심한 사이에 쨈미몬이 나타났습니다. 어서 공격하세요!")

    async def attack(self, interaction: discord.Interaction, damage: int):
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

        success_chance = random.randint(10, 90)
        actual_chance = random.randint(10, 90)
        attack_success = actual_chance <= success_chance

        # 크리티컬 확률 계산
        critical_chance = random.randint(1, 100)
        critical_success = critical_chance <= player["critical"]
        
        if attack_success:
            enemy["hp"] -= damage
            result = (f"공격 성공! 쨈미몬이 {damage}의 데미지를 입었습니다. ( 성공 확률 : {success_chance}% )\n"
                      "( 쨈미몬 : 으앙 )\n"
                      f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}")
            
            if enemy["hp"] <= 0:
                exp_gain = random.randint(30, 40)
                player["exp"] += exp_gain

                if player["exp"] >= player["level"] * 100:
                    player["hp"] = 100
                    player["level"] += 1
                    enemy["hp"] = 40 + 10 * player["level"]
                    
                    result += (f"\n \n레벨 업! 현재 레벨 : {player['level']}"
                               "\n \n와아~ 쨈미몬이 쓰러졌습니다!\n"
                               "...\n"
                               "헉.. 쨈미몬이 더 강해져서 돌아왔어요! 끄앙\n"
                               f"현재 쨈미몬의 체력 : {enemy['hp']}")
                else:
                    player["hp"] = 100
                    enemy["hp"] = 40 + 10 * player["level"]
                    result += ("\n \n와아~ 쨈미몬이 쓰러졌습니다!\n"
                               "...\n"
                               "헉.. 쨈미몬이 다시 깨어났어요!\n"
                               f"현재 쨈미몬의 체력 : {enemy['hp']}")          
        else:
            player["hp"] -= damage
            result = (f"공격 실패! 쨈미몬이 반격해 {damage}의 데미지를 입혔습니다. ( 성공 확률 : {success_chance}% )\n"
                      f"레벨 : {player['level']}, {user_nickname}님의 체력 : {player['hp']}, 쨈미몬의 체력 : {enemy['hp']}")
            if player["hp"] <= 0:
                result += f"\n \n{user_nickname}님의 체력이 0이 되어 사망했습니다. 끄앙"
                self.delete_player_data(user_id)
                await interaction.response.send_message(result)
                return
        
        self.save_game_data(data)
        await interaction.response.send_message(result)

    async def stats(self, interaction: discord.Interaction):
        data = self.load_game_data()
        guild = interaction.guild
        user_nickname = get_user_nickname(guild, interaction.user.id)
        user_id = str(interaction.user.id)
        
        player_data = data.get("players", {}).get(user_id, None)
        enemy_data = data.get("current_enemies", {}).get(user_id, None)
        
        if player_data:
            await interaction.response.send_message(f"[{user_nickname}님의 스탯] \n"
                                                    f"\n레벨 : {player_data['level']}, 체력 : {player_data['hp']}, 경험치 : {player_data['exp']}\n"
                                                    f"현재 쨈미몬의 체력 : {enemy_data['hp']}")
        else:
            await interaction.response.send_message(f"{user_nickname}님의 데이터가 없습니다. `/rpg`로 게임을 시작해보세요!.")

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
            leaderboard_message += f"{rank}. {user_nickname} - 레벨: {player['level']}, 경험치: {player['exp']}\n"

        await interaction.response.send_message(leaderboard_message)
            
