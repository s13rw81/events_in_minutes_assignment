from datetime import datetime

from beanie import Document


class UserExternal(Document):
    name: str
    username: str
    email: str
    created_at: datetime = datetime.now()

    def __str__(self):
        return f"name:{self.name}, created_at: {self.created_at}"

    class Settings:
        name = "users"
