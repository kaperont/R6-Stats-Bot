from beanie import Document


class User(Document):
    user_id: int | None = None
    username: str
    platform: str

    class Settings:
        name = 'User'
