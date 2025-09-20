import os

from beanie import init_beanie
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

from database.models.models import AllowedUsersDocument

load_dotenv()

MONGO_DB_STRING = os.getenv('MONGO_DB_STRING')


async def database_init():

    client = AsyncMongoClient(MONGO_DB_STRING)

    # TODO
    # Look into init_beanie function. Provide custom database name.
    # Custom database name that has been provided only stores 2 documents.

    await init_beanie(database=client.db_name, document_models=[AllowedUsersDocument])
