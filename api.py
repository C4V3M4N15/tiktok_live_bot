from flask import Flask, request, jsonify
from firebase import check_user_subscription, add_subscription, remove_subscription

app = Flask(__name__)

@app.route('/check-subscription', methods=['POST'])
def check_subscription():
    data = request.get_json()
    discord_user_id = data.get('discord_user_id')
    if not discord_user_id:
        return jsonify({'error': 'Missing discord_user_id'}), 400

    active = check_user_subscription(discord_user_id)
    return jsonify({'active': active})

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    discord_user_id = data.get('discord_user_id')
    if not discord_user_id:
        return jsonify({'error': 'Missing discord_user_id'}), 400

    add_subscription(discord_user_id)
    return jsonify({'success': True})

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    discord_user_id = data.get('discord_user_id')
    if not discord_user_id:
        return jsonify({'error': 'Missing discord_user_id'}), 400

    remove_subscription(discord_user_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
