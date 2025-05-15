import firebase_admin
from firebase_admin import credentials, firestore
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