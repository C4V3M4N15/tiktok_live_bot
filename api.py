from flask import Flask, request, jsonify
from firebase import update_server_config, get_server_config

app = Flask(__name__)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    discord_user_id = data.get("discord_user_id")
    guild_id = data.get("guild_id")
    if not discord_user_id or not guild_id:
        return jsonify({"error": "Missing parameters"}), 400
    update_server_config(guild_id, {"is_paid": True, "user_id": discord_user_id})
    return jsonify({"success": True})

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    data = request.get_json()
    guild_id = data.get("guild_id")
    if not guild_id:
        return jsonify({"error": "Missing guild_id"}), 400
    update_server_config(guild_id, {"is_paid": False})
    return jsonify({"success": True})

@app.route("/check-subscription", methods=["POST"])
def check_subscription():
    data = request.get_json()
    guild_id = data.get("guild_id")
    if not guild_id:
        return jsonify({"error": "Missing guild_id"}), 400
    config = get_server_config(guild_id)
    return jsonify({"active": config.get("is_paid", False)})