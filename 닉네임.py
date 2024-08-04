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
