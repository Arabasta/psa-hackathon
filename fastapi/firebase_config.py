import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("firebase.json")

try:
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'psa-hackathon-alvin',
        'databaseURL': 'https://psa-hackathon-alvin.firebaseio.com'
    })
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

db = firestore.client()
bucket = storage.bucket()
