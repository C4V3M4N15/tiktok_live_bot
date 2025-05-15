# tools/firestore_manager.py
import argparse
from firebase import get_all_active_configs, update_server_config, get_server_config

def list_configs():
    configs = get_all_active_configs()
    for i, config in enumerate(configs, 1):
        print(f"\n[{i}] TikTok: {config.get('tiktok_username')}, Discord Token: {'✅' if config.get('discord_bot_token') else '❌'}")

def add_or_update_config(server_id, tiktok_username, discord_token):
    update_server_config(server_id, {
        "tiktok_username": tiktok_username,
        "discord_bot_token": discord_token,
        "is_paid": True
    })
    print(f"✅ Added/Updated config for: {tiktok_username} (ID: {server_id})")

def inspect_config(server_id):
    config = get_server_config(server_id)
    if not config:
        print(f"❌ No config found for server ID {server_id}")
    else:
        print(f"\n🔍 Config for {server_id}:\n{config}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Firestore server configs")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List all active server configs")

    add_parser = subparsers.add_parser("add", help="Add or update a server config")
    add_parser.add_argument("--id", required=True)
    add_parser.add_argument("--tiktok", required=True)
    add_parser.add_argument("--token", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect config by server ID")
    inspect_parser.add_argument("--id", required=True)

    args = parser.parse_args()

    if args.command == "list":
        list_configs()
    elif args.command == "add":
        add_or_update_config(args.id, args.tiktok, args.token)
    elif args.command == "inspect":
        inspect_config(args.id)
    else:
        parser.print_help()
