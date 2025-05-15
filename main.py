import asyncio
from threading import Thread
from api import app  # your Flask app
from tiktok_client import start_tiktok_bot
from discord_client import run_discord_bot


def run_flask():
    # Run Flask app on 0.0.0.0 so Render can expose it publicly
    app.run(host="0.0.0.0", port=5000)


async def main():
    # Start Flask in a background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Create async tasks for TikTok and Discord bots
    tiktok_task = asyncio.create_task(start_tiktok_bot())
    discord_task = asyncio.create_task(run_discord_bot())

    # Wait for both to run concurrently (they both block running forever)
    await asyncio.gather(tiktok_task, discord_task)


if __name__ == "__main__":
    asyncio.run(main())
