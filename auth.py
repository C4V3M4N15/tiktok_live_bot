import os
import requests
from flask import Flask, redirect, request, jsonify
from firebase_admin import auth

app = Flask(__name__)

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")


@app.route("/discord-login")
def discord_login():
    discord_auth_url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        "&response_type=code"
        "&scope=identify email"
    )
    return redirect(discord_auth_url)


@app.route("/discord-callback")
def discord_callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    # Exchange code for access token
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify email",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = requests.post(token_url, data=data, headers=headers)
    if token_response.status_code != 200:
        return f"Failed to get token: {token_response.text}", 400

    access_token = token_response.json().get("access_token")
    if not access_token:
        return "No access token found", 400

    # Use access token to get user info
    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_response.status_code != 200:
        return f"Failed to get user info: {user_response.text}", 400

    user_data = user_response.json()
    discord_user_id = user_data["id"]

    # Create Firebase Custom Token
    custom_token = auth.create_custom_token(discord_user_id)

    # Return token (you can also redirect with token in query or a cookie)
    return jsonify({"firebase_custom_token": custom_token.decode("utf-8")})
