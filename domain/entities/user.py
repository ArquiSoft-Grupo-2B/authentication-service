from dataclasses import dataclass

@dataclass
class User:
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
    


