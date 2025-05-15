import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, GiftEvent, LikeEvent, FollowEvent
from config import TIKTOK_USERNAME
from discord_client import send_to_discord

# Initialize the TikTokLive client
tt_client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

# For throttling like spam
recent_likers = set()
LIKE_THROTTLE_SECONDS = 30  # Customize as needed

@tt_client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    try:
        print(f"Connected to @{event.unique_id} (Room ID: {tt_client.room_id})")
        await send_to_discord(f"✅ Connected to @{event.unique_id} (Room ID: {tt_client.room_id})")
    except Exception as e:
        print(f"⚠️ Error in ConnectEvent: {e}")

@tt_client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    try:
        user = event.user.nickname or "Anonymous"
        comment = event.comment or ""
        print(f"{user} -> {comment}")
        await send_to_discord(f"{user} -> {comment}")
    except Exception as e:
        print(f"⚠️ Error in CommentEvent: {e}")

@tt_client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    try:
        gift_name = event.gift.name or "Unknown Gift"
        sender = event.user.nickname or "Anonymous"
        count = getattr(event, "repeat_count", 1)
        print(f"🎁 {sender} sent gift: {gift_name} x{count}")
        await send_to_discord(f"🎁 {sender} sent gift: {gift_name} x{count}")
    except Exception as e:
        print(f"⚠️ Error in GiftEvent: {e}")

@tt_client.on(LikeEvent)
async def on_like(event: LikeEvent):
    try:
        user = event.user.nickname or "Anonymous"
        if user not in recent_likers:
            print(f"❤️ {user} liked the stream!")
            await send_to_discord(f"❤️ {user} liked the stream!")
            recent_likers.add(user)
            asyncio.create_task(remove_liker_after_delay(user))
    except Exception as e:
        print(f"⚠️ Error in LikeEvent: {e}")

async def remove_liker_after_delay(user):
    await asyncio.sleep(LIKE_THROTTLE_SECONDS)
    recent_likers.discard(user)

@tt_client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    try:
        user = event.user.nickname or "Anonymous"
        print(f"✨ {user} followed!")
        await send_to_discord(f"✨ {user} followed!")
    except Exception as e:
        print(f"⚠️ Error in FollowEvent: {e}")

async def start_tiktok_bot():
    try:
        await tt_client.start()
    except Exception as e:
        print(f"❌ Failed to start TikTok client: {e}")
