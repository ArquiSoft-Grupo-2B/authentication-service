import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path="configs/.env")
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")


cred_dict = json.loads(firebase_credentials_json)
cred = credentials.Certificate(cred_dict)

# Inicializar la app de Firebase si no está inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
auth_client = auth
