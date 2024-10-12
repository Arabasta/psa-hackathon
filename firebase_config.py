import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("firebase.json")

try:
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'psa-hack-64826',
        'databaseURL': 'https://psa-hack-64826.firebaseio.com'
    })
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

db = firestore.client()
bucket = storage.bucket()
