import discord
from discord import app_commands
from discord.ext import commands
import datetime
from collections import defaultdict
from dotenv import load_dotenv
import os
# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
import asyncio
load_dotenv()
class AdiPrayBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.response_tally = defaultdict(int)
        self.adipray_keyword = "adipray"
        self.daily_users = defaultdict(set)  # Track users per day
    async def setup_hook(self):
        # Sync commands with Discord
        await self.tree.sync()
        print("Bot is ready and slash commands synced!")

bot = AdiPrayBot()

@bot.tree.command(name="tally_adipray", description="Tally users who sent messages containing 'adipray' in channels")
async def tally_adipray(interaction: discord.Interaction, thread_id: str = None):
    await interaction.response.defer()  # Defer the response as this might take a while
    
    print("Tallying")
    bot.response_tally.clear()
    bot.daily_users.clear()
    # Set the start date (Jan 1st of the previous year)
    now = datetime.datetime.utcnow()
    start_date = datetime.datetime(year=now.year-1, month=1, day=1)     
    # Determine whether to check the entire server or a specific thread
    if thread_id:
        try:
            thread = await bot.fetch_channel(int(thread_id))
            if not isinstance(thread, discord.Thread):
                await interaction.followup.send("Invalid thread ID. Please provide a valid thread ID.")
                return
            channels_to_check = [thread]
        except (ValueError, discord.NotFound):
            await interaction.followup.send("Invalid thread ID. Please provide a valid thread ID.")
            return
    else:
        channels_to_check = interaction.guild.text_channels
    
    # Scan the selected channels
    for channel in channels_to_check:
        try:
            async for message in channel.history(after=start_date, limit=None, oldest_first=True):
                message_date = message.created_at.date() 
                # Check if the keyword exists and the user has not been counted for the same day
                if ("adipray" in message.content.lower() or 
                     'PES2_Pray'.lower() in message.content.lower()):
                     if message.author.id not in bot.daily_users[message_date]:
                         bot.response_tally[message.author.id] += 1
                         bot.daily_users[message_date].add(message.author.id)
                         await asyncio.sleep(0.1)  # Delay between each message
        except discord.Forbidden:
            continue  # Skip channels the bot can't access
    
    # Generate the rankings
    leaderboard = "📊 **'Adipray' Message Tally** 📊\n"
    ranked_users = sorted(bot.response_tally.items(), key=lambda x: x[1], reverse=True)
    
    for idx, (user_id, count) in enumerate(ranked_users, start=1):
        user = await bot.fetch_user(user_id)
        leaderboard += f"{idx}. {user.name}: Prayed a total of {count} time(s)!\n"
    
    print(leaderboard)
    await interaction.followup.send("🥳🥳🥳 LEADERBOARD GENERATED 🥳🥳🥳")

# @bot.tree.command(name="save_tally", description="Save the current tally data to a file")
# async def save_tally(interaction: discord.Interaction):
#     import json
    
#     await interaction.response.defer()
    
#     try:
#         with open("adipray_tally.json", "w") as file:
#             json.dump(bot.response_tally, file)
#         await interaction.followup.send("Tally data saved successfully.")
#     except Exception as e:
#         await interaction.followup.send(f"Error saving tally data: {str(e)}")

@bot.tree.command(name="show_rankings", description="Display the current adipray rankings")
async def show_rankings(interaction: discord.Interaction):
    await interaction.response.defer()
    
    if not bot.response_tally:
        await interaction.followup.send("No tally data available. Use `/tally_adipray` to load data first.")
        return
    
    # Generate the rankings
    leaderboard = (
        "<:adipray:585851270716325890> <:adipray:585851270716325890> <:adipray:585851270716325890> **2024 FRIDAY LEADERBOARD 🎉🎉 "
        "<:adipray:585851270716325890> <:adipray:585851270716325890> <:adipray:585851270716325890> **\n"
    )
    ranked_users = sorted(bot.response_tally.items(), key=lambda x: x[1], reverse=True)
    
    for idx, (user_id, count) in enumerate(ranked_users, start=1):
        user = await bot.fetch_user(user_id)
        leaderboard += f"{idx}. {user.mention}: {count} times\n"
    
    # Send leaderboard to a specific thread
    thread_id = 870695974476062811  # Replace with your thread ID
    try:
        thread = await bot.fetch_channel(thread_id)
        if isinstance(thread, discord.Thread):
            await thread.send(leaderboard)
            await interaction.followup.send("Leaderboard has been sent to the specific thread!")
        else:
            await interaction.followup.send("The provided ID is not a valid thread.")
    except discord.NotFound:
        await interaction.followup.send("Thread not found. Please check the thread ID.")
    except discord.Forbidden:
        await interaction.followup.send("Bot does not have permission to send messages in the specified thread.")


# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
bot.run("")
