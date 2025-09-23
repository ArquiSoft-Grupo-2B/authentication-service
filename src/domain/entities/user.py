from dataclasses import dataclass

@dataclass
class User:
    """
    Represents a user and business rules in the system.
    """
    id: str
    email: str
    alias: str
    password: str
    photo_url: str|None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "password": self.password,
            "photo_url": self.photo_url
        }
    
    def to_dict_no_password(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "photo_url": self.photo_url
        }
    
    def update_email(self, new_email: str) -> None:
        """Update user email."""
        self.email = new_email
    
    def update_alias(self, new_alias: str) -> None:
        """Update user alias."""
        self.alias = new_alias
    
    def update_password(self, new_password: str) -> None:
        """Update user password."""
        self.password = new_password
    
    def update_photo_url(self, new_photo_url: str|None) -> None:
        """Update user photo URL."""
        self.photo_url = new_photo_url

    def validate(self) -> bool:
        """ Validates the user entity based on business rules."""
        if not self.email or not isinstance(self.email, str) or "@" not in self.email:
            return False
        if not self.alias or not isinstance(self.alias, str):
            return False
        if not self.password or not isinstance(self.password, str):
            return False
        return True



