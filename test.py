@tasks.loop(seconds=1)
async def every_write_forum():
    dt = datetime.datetime.now()
    channel = client.get_channel(tchid)
    if (dt.hour == 2) and (dt.minute == 32) and (dt.second > 30):
        await channel.send("test")
        await asyncio.sleep(10)



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

