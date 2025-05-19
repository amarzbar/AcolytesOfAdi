import discord
from discord import app_commands
from discord.ext import commands
import datetime
from collections import defaultdict
from dotenv import load_dotenv
import os
import re
from pymongo import MongoClient

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

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGO_URI"))

PRAYGE_REGEX = re.compile(r"(prayge|adipray|pepepray|PES2_Pray|adipray~1)", re.IGNORECASE)

@bot.tree.command(name="tally_adipray", description="Tally users who sent messages containing prayge emotes in a specific chat and store in MongoDB")
async def tally_adipray(interaction: discord.Interaction, thread_id: str = None):
    await interaction.response.defer()
    print("Tallying")
    if thread_id:
        try:
            thread = await bot.fetch_channel(int(thread_id))
            if not isinstance(thread, (discord.Thread, discord.TextChannel)):
                await interaction.followup.send("Invalid thread ID. Please provide a valid thread or channel ID.")
                return
            channels_to_check = [thread]
        except (ValueError, discord.NotFound):
            await interaction.followup.send("Invalid thread ID. Please provide a valid thread or channel ID.")
            return
    else:
        channels_to_check = interaction.guild.text_channels

    for channel in channels_to_check:
        db = mongo_client[str(channel.id)]
        collection = db["prayge_tally"]
        user_counts = {}
        user_info = {}
        user_weeks = {}  # Track which weeks a user has already been counted
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                if PRAYGE_REGEX.search(message.content):
                    user_id = message.author.id
                    user_name = message.author.name
                    user_display_name = message.author.display_name if hasattr(message.author, 'display_name') else message.author.name
                    user_avatar = getattr(message.author, 'avatar', None)
                    # Map deleted users and 'marz085123' to 'marzofearth' and use the same user_id for all
                    if user_name == 'marz085123' or user_display_name.lower().startswith('deleted user'):
                        user_id = 1122047166811226122
                        user_display_name = 'marzofearth'
                    # Only count if message is on a Friday
                    msg_date = message.created_at.date()
                    if True:  # 4 = Friday
                        week_key = (user_id, msg_date.isocalendar()[1], msg_date.year)
                        if week_key not in user_weeks:
                            user_counts[user_id] = user_counts.get(user_id, 0) + 1
                            user_info[user_id] = {
                                "user_id": user_id,
                                "user_name": user_name,
                                "user_display_name": user_display_name,
                                "avatar": str(user_avatar) if user_avatar else None
                            }
                            user_weeks[week_key] = True
                    await asyncio.sleep(0.01)
        except discord.Forbidden:
            continue
        # Update MongoDB per user (by user_id, user_name, user_display_name, avatar)
        for user_id, count in user_counts.items():
            info = user_info[user_id]
            collection.update_one(
                {"user_id": user_id},
                {"$inc": {"count": count}, "$set": {"user_name": info["user_name"], "user_display_name": info["user_display_name"], "avatar": info["avatar"]}},
                upsert=True
            )
    await interaction.followup.send("Tally complete and stored in MongoDB.")

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
