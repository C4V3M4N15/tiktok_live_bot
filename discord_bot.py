import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

token = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    try:
        await owner.send("Thanks for adding the bot! Set it up here: https://your-dashboard-link")
    except:
        print(f"Couldn't DM {owner.name}")

async def send_discord_message(channel_id: int, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

def run_discord_bot():
    bot.start(token)