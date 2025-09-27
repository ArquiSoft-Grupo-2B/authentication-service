from typing import Optional, List
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.entities.token import Token
from src.infraestructure.db.firebase import auth_client, db
from ..rest.firebase_auth_api import FirebaseAuthAPI
import firebase_admin


class FirebaseUserRepository(UserRepository):
    """Firebase implementation of UserRepository. Uses firebase_admin SDK"""

    def create_user(
        self, email: str, password: str, alias: Optional[str] = None
    ) -> User:
        """Create a new user and store extra info in Firestore."""
        user_auth = auth_client.create_user(
            email=email,
            password=password,
            display_name=alias,
        )

        # Guardar datos extra en Firestore
        user_data = {
            "id": user_auth.uid,
            "email": email,
            "alias": alias,
        }
        db.collection("users").document(user_auth.uid).set(user_data)

        return User(
            id=user_auth.uid,
            email=user_auth.email,
            password="",  # No se retorna el password
            alias=user_auth.display_name,
        )

    def login_user(self, email: str, password: str) -> Optional[Token]:
        firebase_auth_api = FirebaseAuthAPI()
        response = firebase_auth_api.login_user(email, password)
        if response:
            return Token(
                local_id=response.get("localId"),
                email=response.get("email"),
                alias=response.get("displayName"),
                id_token=response.get("idToken"),
                registered=response.get("registered"),
                refresh_token=response.get("refreshToken"),
                expires_in=response.get("expiresIn"),
            )
        return None

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID from Firestore (extra info) + Auth (email)."""
        try:
            user_record = auth_client.get_user(user_id)
            doc = db.collection("users").document(user_id).get()
            alias = (
                doc.to_dict().get("alias") if doc.exists else user_record.display_name
            )
            return User(
                id=user_record.uid,
                email=user_record.email,
                password="",  # Firebase no expone password
                alias=alias,
            )
        except firebase_admin._auth_utils.UserNotFoundError:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email using Auth and Firestore."""
        try:
            user_record = auth_client.get_user_by_email(email)
            doc = db.collection("users").document(user_record.uid).get()
            alias = (
                doc.to_dict().get("alias") if doc.exists else user_record.display_name
            )
            return User(
                id=user_record.uid,
                email=user_record.email,
                password="",
                alias=alias,
            )
        except firebase_admin._auth_utils.UserNotFoundError:
            return None

    def update_user(self, user: User) -> User:
        """Update user in Auth and Firestore."""
        try:
            user_record = auth_client.update_user(
                user.id,
                email=user.email,
                display_name=user.alias,
                password=user.password if user.password else None,
            )

            db.collection("users").document(user.id).update(
                {
                    "email": user.email,
                    "alias": user.alias,
                }
            )

            return User(
                id=user_record.uid,
                email=user_record.email,
                password="",
                alias=user_record.display_name,
            )
        except firebase_admin._auth_utils.UserNotFoundError:
            raise ValueError("User not found")

    def send_password_reset_email(self, email: str) -> dict:
        """Send a password reset email using Firebase Auth REST API."""
        firebase_auth_api = FirebaseAuthAPI()
        return firebase_auth_api.send_password_reset_email(email)

    def delete_user(self, user_id: str) -> None:
        """Delete user from Auth and Firestore."""
        try:
            auth_client.delete_user(user_id)
            db.collection("users").document(user_id).delete()
        except firebase_admin._auth_utils.UserNotFoundError:
            raise ValueError("User not found")

    def list_users(self) -> List[User]:
        """List all users from Auth, merge with Firestore data."""
        users = []
        for user_record in auth_client.list_users().iterate_all():
            doc = db.collection("users").document(user_record.uid).get()
            alias = (
                doc.to_dict().get("alias") if doc.exists else user_record.display_name
            )
            users.append(
                User(
                    id=user_record.uid,
                    email=user_record.email,
                    password="",
                    alias=alias,
                )
            )
        return users
