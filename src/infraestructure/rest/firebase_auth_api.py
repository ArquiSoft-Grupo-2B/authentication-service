from dotenv import load_dotenv
from typing import Optional
import requests
import os
import json

load_dotenv(dotenv_path="configs/.env")

firebase_api_key = os.getenv("API_KEY")


class FirebaseAuthAPI:
    """Class to interact with Firebase Authentication via REST API."""

    def __init__(self):
        self.api_key = firebase_api_key
        self.base_url = "https://identitytoolkit.googleapis.com/v1"

    def login_user(self, email: str, password: str) -> Optional[dict]:
        """Log in a user using email and password."""

        url = f"{self.base_url}/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json()  # Contains idToken, refreshToken, etc.
        else:
            return None
