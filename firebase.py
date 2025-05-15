# firebase.py
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with service account
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def is_server_subscribed(server_id: str) -> bool:
    """
    Check if a Discord server ID has an active subscription.
    """
    docs = db.collection("subscriptions") \
             .where("discord_server_id", "==", server_id) \
             .where("active", "==", True) \
             .stream()

    return any(True for _ in docs)
