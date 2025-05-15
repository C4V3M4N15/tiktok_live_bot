import os
import requests
from flask import Blueprint, redirect, request, jsonify
from firebase_admin import auth

discord_auth = Blueprint("discord_auth", __name__)

DISCORD_CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
DISCORD_CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
DISCORD_REDIRECT_URI = os.environ["DISCORD_REDIRECT_URI"]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")


@discord_auth.route("/auth/discord/login")
def login():
    scope = "identify email"
    discord_oauth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope}"
    )
    return redirect(discord_oauth_url)


@discord_auth.route("/auth/discord/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing code"}), 400

    token_data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify email",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post("https://discord.com/api/oauth2/token", data=token_data, headers=headers)

    if token_res.status_code != 200:
        return jsonify({"error": "Failed to get Discord token"}), 401

    access_token = token_res.json().get("access_token")
    user_res = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_res.status_code != 200:
        return jsonify({"error": "Failed to get Discord user"}), 401

    user_info = user_res.json()
    discord_uid = user_info["id"]

    try:
        user = auth.get_user(discord_uid)
    except auth.UserNotFoundError:
        user = auth.create_user(
            uid=discord_uid,
            display_name=user_info.get("username"),
            photo_url=f"https://cdn.discordapp.com/avatars/{discord_uid}/{user_info.get('avatar')}.png",
        )

    firebase_token = auth.create_custom_token(discord_uid)
    return jsonify({"firebase_token": firebase_token.decode("utf-8")})
