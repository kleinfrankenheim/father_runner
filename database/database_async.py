import os

from beanie import init_beanie
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

from database.models.models import AllowedUsersDocument

load_dotenv()

MONGO_DB_STRING = os.getenv('MONGO_DB_STRING')


async def database_init():

    client = AsyncMongoClient(MONGO_DB_STRING)
    db_name = client['fatherrunner']

    await init_beanie(database=db_name, document_models=[AllowedUsersDocument])
