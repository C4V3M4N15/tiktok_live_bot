import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, LikeEvent

TIKTOK_USERNAME = "jacobviolette2"

tt_client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@tt_client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"[CONNECT] Connected to @{event.unique_id} (Room ID: {tt_client.room_id})")

@tt_client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    print(f"[COMMENT] {event.user.nickname}: {event.comment}")

@tt_client.on(LikeEvent)
async def on_like(event: LikeEvent):
    print(f"[LIKE] {event.user.nickname} liked the stream! Total Likes: {event.like_count}")

async def main():
    print("Starting TikTokLive client...")
    try:
        await tt_client.start()
    except Exception as e:
        print(f"Error running TikTok client: {e}")

if __name__ == "__main__":
    asyncio.run(main())
