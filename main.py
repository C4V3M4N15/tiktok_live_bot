import asyncio
from threading import Thread
from api import app
from tiktok_bot import start_tiktok_bot
from discord_bot import run_discord_bot
from firebase import get_all_active_configs


def run_flask():
    app.run(host="0.0.0.0", port=5000)


async def main():
    # Start Flask server in background thread immediately
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    configs = get_all_active_configs()
    tasks = []

    for config in configs:
        tiktok_username = config.get("tiktok_username")
        if not tiktok_username:
            print(f"Skipping config missing username: {config}")
            continue

        tasks.append(asyncio.create_task(start_tiktok_bot(tiktok_username, config)))

        # Optional: add discord bot task if you have discord config
        # if discord token in config:
        #    tasks.append(asyncio.create_task(run_discord_bot(config)))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No active bot tasks to run.")


if __name__ == "__main__":
    asyncio.run(main())
