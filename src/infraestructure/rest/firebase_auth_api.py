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
            raise ValueError("Invalid login credentials")

    def send_password_reset_email(self, email: str) -> dict:
        """Send a password reset email to the user."""

        url = f"{self.base_url}/accounts:sendOobCode?key={self.api_key}"
        payload = {"requestType": "PASSWORD_RESET", "email": email}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return {"success": True, "response": response.json().get("email")}
        raise ValueError("Failed to send password reset email")

    def refresh_id_token(self, refresh_token: str) -> Optional[dict]:
        """Refresh the ID token using the refresh token."""

        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()  # Contains new idToken, refreshToken, etc.
        else:
            raise ValueError("Failed to refresh ID token")
