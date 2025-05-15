import asyncio
from collections import defaultdict
from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from firebase import get_all_active_configs
from discord_bot import send_discord_message

user_like_counts = defaultdict(int)
LIKE_RESET_INTERVAL = 60

async def like_reset_loop():
    while True:
        await asyncio.sleep(LIKE_RESET_INTERVAL)
        user_like_counts.clear()

async def handle_events(client: TikTokLiveClient, config: dict):
    discord_channel_id = int(config["discord_channel_id"])

    @client.on("comment")
    async def on_comment(event):
        msg = f"💬 {event.user.nickname}: {event.comment}"
        await send_discord_message(discord_channel_id, msg)

    @client.on("gift")
    async def on_gift(event):
        if event.gift and event.gift.info:
            msg = f"🏱 {event.user.nickname} sent gift: {event.gift.info.name} x{event.gift.count}"
            await send_discord_message(discord_channel_id, msg)

    @client.on("follow")
    async def on_follow(event):
        msg = f"➕ {event.user.nickname} followed!"
        await send_discord_message(discord_channel_id, msg)

    @client.on("like")
    async def on_like(event):
        user_like_counts[event.user.unique_id] += event.like_count or 1
        msg = f"❤️ {event.user.nickname} liked the stream ({user_like_counts[event.user.unique_id]} total)"
        await send_discord_message(discord_channel_id, msg)

async def start_tiktok_bot():
    configs = get_all_active_configs()
    if not configs:
        print("[TikTokBot] No active configs found.")
        return

    tasks = []

    for config in configs:
        username = config["tiktok_username"]
        print(f"[TikTokBot] Starting stream listener for: {username}")

        client = TikTokLiveClient(unique_id=username, log_level=LogLevel.ERROR)
        await handle_events(client, config)

        # Run the TikTok client in a background thread
        loop = asyncio.get_event_loop()
        tasks.append(loop.run_in_executor(None, client.run))

    # Add the like-reset task
    tasks.append(asyncio.create_task(like_reset_loop()))

    await asyncio.gather(*tasks)
