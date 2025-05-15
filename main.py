import asyncio
from threading import Thread
from api import app
from tiktok_bot import start_tiktok_bot
from discord_bot import run_discord_bot
from firebase import get_all_active_configs

def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def main():
    configs = get_all_active_configs()
    tasks = []

    for config in configs:
        discord_token = config.get("discord_bot_token")
        tiktok_username = config.get("tiktok_username")

        if not discord_token or not tiktok_username:
            print(f"skipping config: Missing token or username: {config}")
            continue

        print(f"[+] Launching for {tiktok_username}")
        tasks.append(asyncio.create_task(start_tiktok_bot(tiktok_username)))
        tasks.append(asyncio.create_task(run_discord_bot(discord_token)))


    await asyncio.gather(*tasks)

    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

if __name__ == "__main__":
    asyncio.run(main())