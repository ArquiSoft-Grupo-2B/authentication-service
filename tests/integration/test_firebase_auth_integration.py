"""
Integration tests for Firebase Authentication and Token management.
These tests interact with actual Firebase Authentication services.
"""

import pytest
import time
from src.domain.entities.user import User
from src.domain.entities.token import Token
from src.domain.services.user_service import UserService
from src.domain.services.token_service import TokenService


@pytest.mark.integration
class TestFirebaseAuthenticationIntegration:
    """Integration tests for authentication and token management with Firebase."""

    def test_login_user_success(
        self,
        user_service,
        token_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test user login with valid credentials."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act
        token = user_service.login_user(
            email=test_user_data["email"], password=test_user_data["password"]
        )

        # Assert
        assert token is not None
        assert isinstance(token, Token)
        assert token.email == test_user_data["email"]
        assert token.local_id == created_user.id
        assert token.id_token is not None
        assert token.refresh_token is not None
        assert token.expires_in is not None
        assert token.registered is True

    def test_login_user_invalid_credentials(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test login with invalid password."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act & Assert - Try to login with wrong password
        with pytest.raises(ValueError, match="Login failed"):
            user_service.login_user(
                email=test_user_data["email"], password="WrongPassword123!"
            )

    def test_login_user_nonexistent_user(
        self, user_service, skip_if_no_firebase_config
    ):
        """Test login with non-existent user."""
        # Act & Assert
        with pytest.raises(ValueError, match="No user found with this email"):
            user_service.login_user(
                email="nonexistent@example.com", password="SomePassword123!"
            )

    def test_verify_token_valid(
        self,
        user_service,
        token_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test verifying a valid token."""
        # Arrange - Create user and login to get token
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        login_token = user_service.login_user(
            email=test_user_data["email"], password=test_user_data["password"]
        )

        # Act
        verified_token = token_service.verify_token(login_token.id_token)

        # Assert
        assert verified_token is not None
        assert verified_token.get("uid") == created_user.id
        assert verified_token.get("email") == test_user_data["email"]

    def test_verify_token_invalid(self, token_service, skip_if_no_firebase_config):
        """Test verifying an invalid token."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid token"):
            token_service.verify_token("invalid-token-string")

    def test_verify_token_malformed(self, token_service, skip_if_no_firebase_config):
        """Test verifying a malformed token."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid token"):
            token_service.verify_token("malformed.token.here")

    def test_refresh_token_success(
        self,
        user_service,
        token_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test refreshing a valid refresh token."""
        # Arrange - Create user and login to get tokens
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        login_token = user_service.login_user(
            email=test_user_data["email"], password=test_user_data["password"]
        )

        # Act
        refreshed_tokens = token_service.refresh_token(login_token.refresh_token)

        # Assert
        assert refreshed_tokens is not None
        assert (
            refreshed_tokens.get("access_token") is not None
            or refreshed_tokens.get("id_token") is not None
        )
        assert refreshed_tokens.get("refresh_token") is not None

    def test_refresh_token_invalid(self, token_service, skip_if_no_firebase_config):
        """Test refreshing with an invalid refresh token."""
        # Act & Assert
        with pytest.raises(ValueError, match="Error refreshing token"):
            token_service.refresh_token("invalid-refresh-token")

    def test_refresh_token_expired(self, token_service, skip_if_no_firebase_config):
        """Test refreshing with an expired/malformed refresh token."""
        # Act & Assert
        with pytest.raises(ValueError, match="Error refreshing token"):
            token_service.refresh_token("expired.or.malformed.refresh.token")

    def test_authentication_flow_complete(
        self,
        user_service,
        token_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test complete authentication flow: create user, login, verify token, refresh token."""
        created_user = None
        try:
            # Step 1: Create user
            created_user = user_service.create_user(
                email=test_user_data["email"],
                password=test_user_data["password"],
                alias=test_user_data["alias"],
            )
            assert created_user is not None

            # Step 2: Login user
            login_token = user_service.login_user(
                email=test_user_data["email"], password=test_user_data["password"]
            )
            assert login_token is not None
            assert login_token.id_token is not None
            assert login_token.refresh_token is not None

            # Step 3: Verify token
            verified_token = token_service.verify_token(login_token.id_token)
            assert verified_token is not None
            assert verified_token.get("uid") == created_user.id

            # Step 4: Refresh token
            refreshed_tokens = token_service.refresh_token(login_token.refresh_token)
            assert refreshed_tokens is not None

            # Step 5: Verify refreshed token works
            new_id_token = refreshed_tokens.get("id_token") or refreshed_tokens.get(
                "access_token"
            )
            if new_id_token:
                verified_refreshed_token = token_service.verify_token(new_id_token)
                assert verified_refreshed_token is not None
                assert verified_refreshed_token.get("uid") == created_user.id

            # Step 6: Send password reset email
            reset_result = user_service.send_password_reset_email(
                test_user_data["email"]
            )
            assert reset_result.get("success") is True

            # Cleanup
            user_service.delete_user(created_user.id)

        except Exception as e:
            # Cleanup in case of test failure
            if created_user and created_user.id:
                try:
                    user_service.delete_user(created_user.id)
                except:
                    pass
            raise e

    def test_multiple_users_authentication(
        self, user_service, token_service, test_user_data, skip_if_no_firebase_config
    ):
        """Test authentication with multiple users to ensure no interference."""
        user1_data = test_user_data.copy()
        user2_data = {
            "email": f"second-{test_user_data['email']}",
            "password": "SecondPassword123!",
            "alias": "SecondUser",
        }

        created_users = []
        try:
            # Create two users
            user1 = user_service.create_user(
                email=user1_data["email"],
                password=user1_data["password"],
                alias=user1_data["alias"],
            )
            created_users.append(user1.id)

            user2 = user_service.create_user(
                email=user2_data["email"],
                password=user2_data["password"],
                alias=user2_data["alias"],
            )
            created_users.append(user2.id)

            # Login both users
            token1 = user_service.login_user(
                user1_data["email"], user1_data["password"]
            )
            token2 = user_service.login_user(
                user2_data["email"], user2_data["password"]
            )

            # Verify both tokens work independently
            verified1 = token_service.verify_token(token1.id_token)
            verified2 = token_service.verify_token(token2.id_token)

            assert verified1.get("uid") == user1.id
            assert verified2.get("uid") == user2.id
            assert verified1.get("email") == user1_data["email"]
            assert verified2.get("email") == user2_data["email"]

            # Cleanup
            for user_id in created_users:
                user_service.delete_user(user_id)

        except Exception as e:
            # Cleanup in case of test failure
            for user_id in created_users:
                try:
                    user_service.delete_user(user_id)
                except:
                    pass
            raise e

    def test_token_verification_after_user_deletion(
        self, user_service, token_service, test_user_data, skip_if_no_firebase_config
    ):
        """Test that tokens become invalid after user deletion."""
        # Arrange - Create user and get token
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )

        login_token = user_service.login_user(
            email=test_user_data["email"], password=test_user_data["password"]
        )

        # Verify token works initially
        verified_token = token_service.verify_token(login_token.id_token)
        assert verified_token is not None

        # Delete user
        user_service.delete_user(created_user.id)

        # Verify token no longer works
        # Note: This might take some time to propagate in Firebase
        with pytest.raises(ValueError):
            token_service.verify_token(login_token.id_token)

    def test_concurrent_login_attempts(
        self,
        user_service,
        test_user_data,
        test_users_cleanup,
        skip_if_no_firebase_config,
    ):
        """Test multiple concurrent login attempts with same user."""
        # Arrange - Create a user first
        created_user = user_service.create_user(
            email=test_user_data["email"],
            password=test_user_data["password"],
            alias=test_user_data["alias"],
        )
        test_users_cleanup.append(created_user.id)

        # Act - Multiple login attempts
        tokens = []
        for i in range(3):
            token = user_service.login_user(
                email=test_user_data["email"], password=test_user_data["password"]
            )
            tokens.append(token)
            time.sleep(0.1)  # Small delay between requests

        # Assert - All tokens should be valid but different
        assert len(tokens) == 3
        for token in tokens:
            assert token is not None
            assert token.local_id == created_user.id
            assert token.email == test_user_data["email"]

        # Tokens should have different values (Firebase generates new tokens each time)
        token_strings = [token.id_token for token in tokens]
        assert len(set(token_strings)) == 3  # All tokens should be unique
