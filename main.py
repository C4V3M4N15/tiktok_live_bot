import asyncio
from threading import Thread
from api import app
from tiktok_bot import start_tiktok_bot
from discord_bot import run_discord_bot

def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def main():
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    tiktok_task = asyncio.create_task(start_tiktok_bot())
    discord_task = asyncio.create_task(run_discord_bot())
    await asyncio.gather(tiktok_task, discord_task)

if __name__ == "__main__":
    asyncio.run(main())