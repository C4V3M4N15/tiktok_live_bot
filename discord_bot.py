import os
import discord
from discord.ext import commands

def create_discord_bot():
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot

bot = create_discord_bot()

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    try:
        await owner.send("Thanks for adding the bot! Set it up here: https://your-dashboard-link")
    except Exception:
        print(f"Couldn't DM {owner.name}")

async def send_discord_message(channel_id: int, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

async def run_discord_bot(server_config):
    token = server_config.get("discord_bot_token")
    if not token:
        raise ValueError("Missing discord bot token in server config")
    await bot.start(token)
