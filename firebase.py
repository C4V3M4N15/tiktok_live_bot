import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

cred_data = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_all_active_configs():
    docs = db.collection("servers").where("is_paid", "==", True).stream()
    return [doc.to_dict() for doc in docs]

def get_server_config(server_id):
    doc = db.collection("servers").document(str(server_id)).get()
    return doc.to_dict() if doc.exists else None

def update_server_config(server_id, data):
    db.collection("servers").document(str(server_id)).set(data, merge=True)

def save_user_settings(uid, discord_channel_id, tiktok_username):
    settings_ref = db.collection('user_settings').document(uid)
    settings_ref.set({
        'discord_channel_id': discord_channel_id,
        'tiktok_username': tiktok_username
    })

def get_user_settings(uid):
    settings_ref = db.collection('user_settings').document(uid)
    doc = settings_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_user(uid):
    try:
        return auth.get_user(uid)
    except auth.UserNotFoundError:
        return None