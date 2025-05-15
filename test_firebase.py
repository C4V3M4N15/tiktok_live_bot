import os
import json

cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "/run/secrets/serviceAccountKey.json")
print(f"Looking for Firebase credentials at: {cred_path}")

with open(cred_path, "r") as f:
    data = json.load(f)
    print("✅ Firebase credentials loaded successfully!")
