from beanie import Document
from pydantic import BaseModel, Field


class AllowedUsersDocument(Document):

    # Matches to document name in MongoDB database.
    class Settings:
        name = 'ai_allowed_users'

    tg_id: int


class AllowedUsersDocumentView(BaseModel):

    tg_id: int

