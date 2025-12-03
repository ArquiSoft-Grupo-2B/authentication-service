import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os
import json
load_dotenv()
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

cred = credentials.Certificate(firebase_credentials_path)

# Inicializar la app de Firebase si no está inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
auth_client = auth
