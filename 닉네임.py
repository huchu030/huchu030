def get_user_nickname(guild, user_id):
    member = guild.get_member(user_id)
    if member:
        return member.display_name
    return "Unknown"


guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)

{user_nickname}

data = self.load_game_data()
        if user_id in data["players"]:
            if user_id not in data["players"]:




    def add_new_player(self, user_id):
        data = self.load_game_data()
        if user_id not in data["players"]:
            data["players"][user_id] = {
                "level": 1,
                "hp": 100,
                "exp": 0,
                "attack": 0,
                "defense": 0,
                "evasion_chance": 0,
                "critical_chance": 0,
                "critical_damage": 0.5,
                "coins": 0,
                "evasion_items" : 0
            }
            data["current_enemies"][user_id] = {
                "hp": 50
            }
            self.save_game_data(data)





        @discord.ui.button(label="버섯", style=discord.ButtonStyle.primary, custom_id="shop_attack")
        async def shop_attack(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_attack")

        @discord.ui.button(label="고양이", style=discord.ButtonStyle.primary, custom_id="shop_defense")
        async def shop_defense(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_defense")

        @discord.ui.button(label="네잎클로버", style=discord.ButtonStyle.primary, custom_id="shop_evasion")
        async def shop_evasion(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_evasion")

        @discord.ui.button(label="안경", style=discord.ButtonStyle.primary, custom_id="shop_critical")
        async def shop_critical(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_critical")

        @discord.ui.button(label="민트초코", style=discord.ButtonStyle.primary, custom_id="shop_critical_damage")
        async def shop_critical_damage(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_critical_damage")

        @discord.ui.button(label="수학의 정석", style=discord.ButtonStyle.primary, custom_id="shop_evasion_item")
        async def shop_evasion_item(self, button: discord.ui.Button, interaction: discord.Interaction):
            await self.purchase_item(interaction, "shop_evasion_item")


