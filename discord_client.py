# discord_client.py
import discord
from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from firebase import is_server_subscribed  # ← add this

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def send_to_discord(message):
    # Check subscription status before posting
    if not is_server_subscribed(str(DISCORD_CHANNEL_ID)):
        print("Subscription inactive. Message not sent.")
        return

    channel = client.get_channel(int(DISCORD_CHANNEL_ID))
    if channel is None:
        try:
            channel = await client.fetch_channel(int(DISCORD_CHANNEL_ID))
        except discord.errors.DiscordException as e:
            print(f"Discord error: {e}")
            return

    await channel.send(message)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

def run_discord_bot():
    return client.start(DISCORD_TOKEN)