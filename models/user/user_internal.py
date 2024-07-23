from datetime import datetime

from beanie import Document


class UserInternal(Document):
    name: str
    username: str
    email: str
    password: str
    created_at: datetime = datetime.now()
    admin: bool = False

    def __str__(self):
        return f"name:{self.name}, created_at: {self.created_at}"

    class Settings:
        name = "users"

