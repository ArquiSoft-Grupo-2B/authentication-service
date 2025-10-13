""""""

Integration tests for Firebase User Repository and User Use Cases.Integration tests for Firebase User Repository and User Use Cases.

These tests interact with actual Firebase services.These tests interact with actual Firebase services.

""""""



import pytestimport pytest

import timeimport time

from src.domain.entities.user import Userfrom src.domain.entities.user import User

from src.application.user_use_cases import UserUseCasesfrom src.application.user_use_cases import UserUseCases

from src.infrastructure.repositories.firebase_user_repository import (from src.infrastructure.repositories.firebase_user_repository import (

    FirebaseUserRepository,    FirebaseUserRepository,

))





@pytest.mark.integration@pytest.mark.integration

class TestFirebaseUserIntegration:class TestFirebaseUserIntegration:

    """Integration tests for user management with Firebase."""    """Integration tests for user management with Firebase."""



    def test_create_user_success(    def test_create_user_success(

        self,        self,

        user_use_cases,        user_use_cases,

        test_user_data,        test_user_data,

        test_users_cleanup,        test_users_cleanup,

        skip_if_no_firebase_config,        skip_if_no_firebase_config,

    ):    ):

        """Test creating a user successfully in Firebase."""        """Test creating a user successfully in Firebase."""

        # Act        # Act

        created_user_dict = user_use_cases.create_user(        created_user_dict = user_use_cases.create_user(

            email=test_user_data["email"],            email=test_user_data["email"],

            password=test_user_data["password"],            password=test_user_data["password"],

            alias=test_user_data["alias"],            alias=test_user_data["alias"],

        )        )



        # Add to cleanup list        # Add to cleanup list

        test_users_cleanup.append(created_user_dict["id"])        test_users_cleanup.append(created_user_dict["id"])



        # Assert        # Assert

        assert created_user_dict is not None        assert created_user_dict is not None

        assert created_user_dict["id"] is not None        assert created_user_dict["id"] is not None

        assert created_user_dict["email"] == test_user_data["email"]        assert created_user_dict["email"] == test_user_data["email"]

        assert created_user_dict["alias"] == test_user_data["alias"]        assert created_user_dict["alias"] == test_user_data["alias"]

        assert "password" not in created_user_dict  # Password should not be returned        assert "password" not in created_user_dict  # Password should not be returned



    def test_create_user_without_alias(    def test_create_user_without_alias(

        self,        self,

        user_use_cases,        user_service,

        test_user_data_no_alias,        test_user_data_no_alias,

        test_users_cleanup,        test_users_cleanup,

        skip_if_no_firebase_config,        skip_if_no_firebase_config,

    ):    ):

        """Test creating a user without alias."""        """Test creating a user without alias."""

        # Act        # Act

        created_user_dict = user_use_cases.create_user(        created_user = user_service.create_user(

            email=test_user_data_no_alias["email"],            email=test_user_data_no_alias["email"],

            password=test_user_data_no_alias["password"],            password=test_user_data_no_alias["password"],

            alias=test_user_data_no_alias["alias"],            alias=test_user_data_no_alias["alias"],

        )        )



        # Add to cleanup list        # Add to cleanup list

        test_users_cleanup.append(created_user_dict["id"])        test_users_cleanup.append(created_user.id)



        # Assert        # Assert

        assert created_user_dict is not None        assert created_user is not None

        assert created_user_dict["id"] is not None        assert created_user.id is not None

        assert created_user_dict["email"] == test_user_data_no_alias["email"]        assert created_user.email == test_user_data_no_alias["email"]

        assert created_user_dict["alias"] is None        assert created_user.alias is None



    def test_create_user_duplicate_email_fails(    def test_create_user_duplicate_email_fails(

        self,        self,

        user_use_cases,        user_service,

        test_user_data,        test_user_data,

        test_users_cleanup,        test_users_cleanup,

        skip_if_no_firebase_config,        skip_if_no_firebase_config,

    ):    ):

        """Test that creating a user with duplicate email fails."""        """Test that creating a user with duplicate email fails."""

        # Arrange - Create first user        # Arrange - Create first user

        created_user_dict = user_use_cases.create_user(        created_user = user_service.create_user(

            email=test_user_data["email"],            email=test_user_data["email"],

            password=test_user_data["password"],            password=test_user_data["password"],

            alias=test_user_data["alias"],            alias=test_user_data["alias"],

        )        )

        test_users_cleanup.append(created_user_dict["id"])        test_users_cleanup.append(created_user.id)



        # Act & Assert - Try to create user with same email        # Act & Assert - Try to create user with same email

        with pytest.raises(ValueError, match="User with this email already exists"):        with pytest.raises(ValueError, match="User with this email already exists"):

            user_use_cases.create_user(            user_service.create_user(

                email=test_user_data["email"],                email=test_user_data["email"],

                password="DifferentPassword123!",                password="DifferentPassword123!",

                alias="DifferentAlias",                alias="DifferentAlias",

            )            )



    def test_create_user_invalid_data_fails(    def test_create_user_invalid_data_fails(

        self, user_use_cases, invalid_test_user_data, skip_if_no_firebase_config        self, user_service, invalid_test_user_data, skip_if_no_firebase_config

    ):    ):

        """Test that creating users with invalid data fails."""        """Test that creating users with invalid data fails."""

        for invalid_data in invalid_test_user_data:        for invalid_data in invalid_test_user_data:

            with pytest.raises(Exception):  # Could be ValueError or Firebase exception            with pytest.raises(Exception):  # Could be ValueError or Firebase exception

                user_use_cases.create_user(                user_service.create_user(

                    email=invalid_data["email"],                    email=invalid_data["email"],

                    password=invalid_data["password"],                    password=invalid_data["password"],

                    alias=invalid_data["alias"],                    alias=invalid_data["alias"],

                )                )



    def test_get_user_by_id_success(    def test_get_user_by_id_success(

        self,        self,

        user_use_cases,        user_service,

        test_user_data,        test_user_data,

        test_users_cleanup,        test_users_cleanup,

        skip_if_no_firebase_config,        skip_if_no_firebase_config,

    ):    ):

        """Test getting a user by ID successfully."""        """Test getting a user by ID successfully."""

        # Arrange - Create a user first        # Arrange - Create a user first

        created_user_dict = user_use_cases.create_user(        created_user = user_service.create_user(

            email=test_user_data["email"],            email=test_user_data["email"],

            password=test_user_data["password"],            password=test_user_data["password"],

            alias=test_user_data["alias"],            alias=test_user_data["alias"],

        )        )

        test_users_cleanup.append(created_user_dict["id"])        test_users_cleanup.append(created_user.id)



        # Act        # Act

        retrieved_user_dict = user_use_cases.get_user(created_user_dict["id"])        retrieved_user = user_service.get_user(created_user.id)



        # Assert        # Assert

        assert retrieved_user_dict is not None        assert retrieved_user is not None

        assert retrieved_user_dict["id"] == created_user_dict["id"]        assert retrieved_user.id == created_user.id

        assert retrieved_user_dict["email"] == created_user_dict["email"]        assert retrieved_user.email == created_user.email

        assert retrieved_user_dict["alias"] == created_user_dict["alias"]        assert retrieved_user.alias == created_user.alias



    def test_get_user_by_id_not_found(self, user_use_cases, skip_if_no_firebase_config):    def test_get_user_by_id_not_found(self, user_service, skip_if_no_firebase_config):

        """Test getting a non-existent user by ID."""        """Test getting a non-existent user by ID."""

        # Act        # Act & Assert

        result = user_use_cases.get_user("non-existent-user-id")        with pytest.raises(ValueError, match="User not found"):

            user_service.get_user("non-existent-user-id")

        # Assert

        assert result is None    def test_get_user_by_email_success(

        self,

    def test_get_user_by_email_success(        user_service,

        self,        test_user_data,

        user_use_cases,        test_users_cleanup,

        test_user_data,        skip_if_no_firebase_config,

        test_users_cleanup,    ):

        skip_if_no_firebase_config,        """Test getting a user by email successfully."""

    ):        # Arrange - Create a user first

        """Test getting a user by email successfully."""        created_user = user_service.create_user(

        # Arrange - Create a user first            email=test_user_data["email"],

        created_user_dict = user_use_cases.create_user(            password=test_user_data["password"],

            email=test_user_data["email"],            alias=test_user_data["alias"],

            password=test_user_data["password"],        )

            alias=test_user_data["alias"],        test_users_cleanup.append(created_user.id)

        )

        test_users_cleanup.append(created_user_dict["id"])        # Act

        retrieved_user = user_service.get_user_by_email(test_user_data["email"])

        # Act

        retrieved_user = user_use_cases.get_user_by_email(test_user_data["email"])        # Assert

        assert retrieved_user is not None

        # Assert        assert retrieved_user.id == created_user.id

        assert retrieved_user is not None        assert retrieved_user.email == created_user.email

        assert retrieved_user.id == created_user_dict["id"]        assert retrieved_user.alias == created_user.alias

        assert retrieved_user.email == created_user_dict["email"]

        assert retrieved_user.alias == created_user_dict["alias"]    def test_get_user_by_email_not_found(

        self, user_service, skip_if_no_firebase_config

    def test_get_user_by_email_not_found(    ):

        self, user_use_cases, skip_if_no_firebase_config        """Test getting a non-existent user by email returns None."""

    ):        # Act

        """Test getting a non-existent user by email returns None."""        result = user_service.get_user_by_email("nonexistent@example.com")

        # Act

        result = user_use_cases.get_user_by_email("nonexistent@example.com")        # Assert

        assert result is None

        # Assert

        assert result is None    def test_list_users(

        self,

    def test_list_users(        user_service,

        self,        test_user_data,

        user_use_cases,        test_users_cleanup,

        test_user_data,        skip_if_no_firebase_config,

        test_users_cleanup,    ):

        skip_if_no_firebase_config,        """Test listing all users includes our test user."""

    ):        # Arrange - Get initial count

        """Test listing all users includes our test user."""        initial_users = user_service.list_users()

        # Arrange - Get initial count        initial_count = len(initial_users)

        initial_users = user_use_cases.list_users()

        initial_count = len(initial_users)        # Create a test user

        created_user = user_service.create_user(

        # Create a test user            email=test_user_data["email"],

        created_user_dict = user_use_cases.create_user(            password=test_user_data["password"],

            email=test_user_data["email"],            alias=test_user_data["alias"],

            password=test_user_data["password"],        )

            alias=test_user_data["alias"],        test_users_cleanup.append(created_user.id)

        )

        test_users_cleanup.append(created_user_dict["id"])        # Act

        users_after_creation = user_service.list_users()

        # Act

        users_after_creation = user_use_cases.list_users()        # Assert

        assert len(users_after_creation) == initial_count + 1

        # Assert

        assert len(users_after_creation) == initial_count + 1        # Find our created user in the list

        created_user_in_list = next(

        # Find our created user in the list            (user for user in users_after_creation if user.id == created_user.id), None

        created_user_in_list = next(        )

            (user for user in users_after_creation if user["id"] == created_user_dict["id"]), None        assert created_user_in_list is not None

        )        assert created_user_in_list.email == test_user_data["email"]

        assert created_user_in_list is not None

        assert created_user_in_list["email"] == test_user_data["email"]    def test_update_user_success(

        self,

    def test_update_user_success(        user_service,

        self,        test_user_data,

        user_use_cases,        test_users_cleanup,

        test_user_data,        skip_if_no_firebase_config,

        test_users_cleanup,    ):

        skip_if_no_firebase_config,        """Test updating a user successfully."""

    ):        # Arrange - Create a user first

        """Test updating a user successfully."""        created_user = user_service.create_user(

        # Arrange - Create a user first            email=test_user_data["email"],

        created_user_dict = user_use_cases.create_user(            password=test_user_data["password"],

            email=test_user_data["email"],            alias=test_user_data["alias"],

            password=test_user_data["password"],        )

            alias=test_user_data["alias"],        test_users_cleanup.append(created_user.id)

        )

        test_users_cleanup.append(created_user_dict["id"])        # Modify user data

        updated_user = User(

        # Modify user data            id=created_user.id,

        updated_data = {            email=created_user.email,  # Keep same email to avoid conflicts

            "id": created_user_dict["id"],            password="NewPassword123!",

            "email": created_user_dict["email"],  # Keep same email to avoid conflicts            alias="UpdatedAlias",

            "alias": "UpdatedAlias",        )

        }

        # Act

        # Act        result = user_service.update_user(updated_user)

        result = user_use_cases.update_user(updated_data)

        # Assert

        # Assert        assert result is not None

        assert result is not None        assert result.id == created_user.id

        assert result["id"] == created_user_dict["id"]        assert result.email == created_user.email

        assert result["email"] == created_user_dict["email"]        assert result.alias == "UpdatedAlias"

        assert result["alias"] == "UpdatedAlias"

        # Verify the update persisted

        # Verify the update persisted        retrieved_user = user_service.get_user(created_user.id)

        retrieved_user_dict = user_use_cases.get_user(created_user_dict["id"])        assert retrieved_user.alias == "UpdatedAlias"

        assert retrieved_user_dict["alias"] == "UpdatedAlias"

    def test_update_user_not_found(self, user_service, skip_if_no_firebase_config):

    def test_update_user_not_found(self, user_use_cases, skip_if_no_firebase_config):        """Test updating a non-existent user fails."""

        """Test updating a non-existent user fails."""        # Arrange

        # Arrange        non_existent_user = User(

        non_existent_user_data = {            id="non-existent-id",

            "id": "non-existent-id",            email="test@example.com",

            "email": "test@example.com",            password="password123",

            "alias": "alias",            alias="alias",

        }        )



        # Act & Assert        # Act & Assert

        with pytest.raises(ValueError, match="User not found"):        with pytest.raises(ValueError, match="User not found"):

            user_use_cases.update_user(non_existent_user_data)            user_service.update_user(non_existent_user)



    def test_update_user_email_conflict(    def test_update_user_email_conflict(

        self,        self,

        user_use_cases,        user_service,

        test_user_data,        test_user_data,

        test_users_cleanup,        test_users_cleanup,

        skip_if_no_firebase_config,        skip_if_no_firebase_config,

    ):    ):

        """Test updating user with email that belongs to another user fails."""        """Test updating user with email that belongs to another user fails."""

        # Arrange - Create two users        # Arrange - Create two users

        user1_data = test_user_data.copy()        user1_data = test_user_data.copy()

        user1_dict = user_use_cases.create_user(        user1 = user_service.create_user(

            email=user1_data["email"],            email=user1_data["email"],

            password=user1_data["password"],            password=user1_data["password"],

            alias=user1_data["alias"],            alias=user1_data["alias"],

        )        )

        test_users_cleanup.append(user1_dict["id"])        test_users_cleanup.append(user1.id)



        user2_data = {        user2_data = {

            "email": f"second-{user1_data['email']}",            "email": f"second-{user1_data['email']}",

            "password": "Password123!",            "password": "Password123!",

            "alias": "SecondUser",            "alias": "SecondUser",

        }        }

        user2_dict = user_use_cases.create_user(        user2 = user_service.create_user(

            email=user2_data["email"],            email=user2_data["email"],

            password=user2_data["password"],            password=user2_data["password"],

            alias=user2_data["alias"],            alias=user2_data["alias"],

        )        )

        test_users_cleanup.append(user2_dict["id"])        test_users_cleanup.append(user2.id)



        # Try to update user2 with user1's email        # Try to update user2 with user1's email

        user2_with_conflicting_email = {        user2_with_conflicting_email = User(

            "id": user2_dict["id"],            id=user2.id,

            "email": user1_dict["email"],  # This should cause conflict            email=user1.email,  # This should cause conflict

            "alias": "UpdatedUser2",            password="NewPassword123!",

        }            alias="UpdatedUser2",

        )

        # Act & Assert

        with pytest.raises(ValueError, match="Email already in use"):        # Act & Assert

            user_use_cases.update_user(user2_with_conflicting_email)        with pytest.raises(ValueError, match="Email already in use"):

            user_service.update_user(user2_with_conflicting_email)

    def test_send_password_reset_email_success(

        self,    def test_send_password_reset_email_success(

        user_use_cases,        self,

        test_user_data,        user_service,

        test_users_cleanup,        test_user_data,

        skip_if_no_firebase_config,        test_users_cleanup,

    ):        skip_if_no_firebase_config,

        """Test sending password reset email for existing user."""    ):

        # Arrange - Create a user first        """Test sending password reset email for existing user."""

        created_user_dict = user_use_cases.create_user(        # Arrange - Create a user first

            email=test_user_data["email"],        created_user = user_service.create_user(

            password=test_user_data["password"],            email=test_user_data["email"],

            alias=test_user_data["alias"],            password=test_user_data["password"],

        )            alias=test_user_data["alias"],

        test_users_cleanup.append(created_user_dict["id"])        )

        test_users_cleanup.append(created_user.id)

        # Act

        result = user_use_cases.send_password_reset_email(test_user_data["email"])        # Act

        result = user_service.send_password_reset_email(test_user_data["email"])

        # Assert

        assert result is not None        # Assert

        # The exact structure depends on your Firebase implementation        assert result is not None

        assert result.get("success") is True

    def test_send_password_reset_email_user_not_found(

        self, user_use_cases, skip_if_no_firebase_config    def test_send_password_reset_email_user_not_found(

    ):        self, user_service, skip_if_no_firebase_config

        """Test sending password reset email for non-existent user fails."""    ):

        # Act & Assert        """Test sending password reset email for non-existent user fails."""

        with pytest.raises(ValueError, match="No user found with this email"):        # Act & Assert

            user_use_cases.send_password_reset_email("nonexistent@example.com")        with pytest.raises(ValueError, match="No user found with this email"):

            user_service.send_password_reset_email("nonexistent@example.com")

    def test_send_password_reset_email_invalid_format(

        self, user_use_cases, skip_if_no_firebase_config    def test_send_password_reset_email_invalid_format(

    ):        self, user_service, skip_if_no_firebase_config

        """Test sending password reset email with invalid email format fails."""    ):

        # Act & Assert        """Test sending password reset email with invalid email format fails."""

        with pytest.raises(ValueError, match="Invalid email format"):        # Act & Assert

            user_use_cases.send_password_reset_email("invalid-email-format")        with pytest.raises(ValueError, match="Invalid email format"):

            user_service.send_password_reset_email("invalid-email-format")

    def test_delete_user_success(

        self, user_use_cases, test_user_data, skip_if_no_firebase_config    def test_delete_user_success(

    ):        self, user_service, test_user_data, skip_if_no_firebase_config

        """Test deleting a user successfully."""    ):

        # Arrange - Create a user first        """Test deleting a user successfully."""

        created_user_dict = user_use_cases.create_user(        # Arrange - Create a user first

            email=test_user_data["email"],        created_user = user_service.create_user(

            password=test_user_data["password"],            email=test_user_data["email"],

            alias=test_user_data["alias"],            password=test_user_data["password"],

        )            alias=test_user_data["alias"],

        )

        # Act

        user_use_cases.delete_user(created_user_dict["id"])        # Act

        user_service.delete_user(created_user.id)

        # Assert - User should no longer exist

        result = user_use_cases.get_user(created_user_dict["id"])        # Assert - User should no longer exist

        assert result is None        with pytest.raises(ValueError, match="User not found"):

            user_service.get_user(created_user.id)

    def test_delete_user_not_found(self, user_use_cases, skip_if_no_firebase_config):

        """Test deleting a non-existent user fails."""    def test_delete_user_not_found(self, user_service, skip_if_no_firebase_config):

        # Act & Assert        """Test deleting a non-existent user fails."""

        with pytest.raises(ValueError, match="User not found"):        # Act & Assert

            user_use_cases.delete_user("non-existent-user-id")        with pytest.raises(ValueError, match="User not found"):

            user_service.delete_user("non-existent-user-id")

    def test_full_user_lifecycle(

        self, user_use_cases, test_user_data, skip_if_no_firebase_config    def test_full_user_lifecycle(

    ):        self, user_service, test_user_data, skip_if_no_firebase_config

        """Test complete user lifecycle: create, read, update, delete."""    ):

        created_user_dict = None        """Test complete user lifecycle: create, read, update, delete."""

        try:        created_user = None

            # Create        try:

            created_user_dict = user_use_cases.create_user(            # Create

                email=test_user_data["email"],            created_user = user_service.create_user(

                password=test_user_data["password"],                email=test_user_data["email"],

                alias=test_user_data["alias"],                password=test_user_data["password"],

            )                alias=test_user_data["alias"],

            assert created_user_dict is not None            )

            assert created_user is not None

            # Read

            retrieved_user_dict = user_use_cases.get_user(created_user_dict["id"])            # Read

            assert retrieved_user_dict["email"] == test_user_data["email"]            retrieved_user = user_service.get_user(created_user.id)

            assert retrieved_user.email == test_user_data["email"]

            # Update

            updated_data = {            # Update

                "id": created_user_dict["id"],            updated_user = User(

                "email": created_user_dict["email"],                id=created_user.id,

                "alias": "UpdatedAlias",                email=created_user.email,

            }                password="NewPassword123!",

            result = user_use_cases.update_user(updated_data)                alias="UpdatedAlias",

            assert result["alias"] == "UpdatedAlias"            )

            result = user_service.update_user(updated_user)

            # Delete            assert result.alias == "UpdatedAlias"

            user_use_cases.delete_user(created_user_dict["id"])

            # Delete

            # Verify deletion            user_service.delete_user(created_user.id)

            result = user_use_cases.get_user(created_user_dict["id"])

            assert result is None            # Verify deletion

            with pytest.raises(ValueError, match="User not found"):

        except Exception as e:                user_service.get_user(created_user.id)

            # Cleanup in case of test failure

            if created_user_dict and created_user_dict.get("id"):        except Exception as e:

                try:            # Cleanup in case of test failure

                    user_use_cases.delete_user(created_user_dict["id"])            if created_user and created_user.id:

                except:                try:

                    pass                    user_service.delete_user(created_user.id)

            raise e                except:
                    pass
            raise e
