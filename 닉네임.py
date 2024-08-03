def get_user_nickname(guild, user_id):
    member = guild.get_member(user_id)
    if member:
        return member.display_name
    return "Unknown"


guild = interaction.guild
    user_nickname = get_user_nickname(guild, interaction.user.id)

{user_nickname}
