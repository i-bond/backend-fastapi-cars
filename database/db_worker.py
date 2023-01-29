import beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.cars import Cars
from models.users import UsersPublic
from models.newsletters import Newsletters
from pprint import pprint
from decouple import config

# Load .env variables
DB_URL = config('DB_URL', default='mongodb://localhost:27017', cast=str)
DB_NAME = config('DB_NAME', default='carsDB', cast=str)


async def connect_db():
    client = AsyncIOMotorClient(DB_URL)
    await beanie.init_beanie(database=client[DB_NAME], document_models=[Cars, UsersPublic, Newsletters])






























