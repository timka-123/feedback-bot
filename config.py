from os import environ

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

mongo = AsyncIOMotorClient(environ.get("MONGO")).datamine
admin_id = environ.get("ADMIN_ID")


class Bot(Bot):
    def __init__(self):
        super().__init__(
            token=environ.get("TOKEN")
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        self.mongo = AsyncIOMotorClient(environ.get("MONGO")).datamine


async def check_user(user_id: int):
    user_data = await mongo.banned.find_one({'_id': user_id})
    return True if user_data else False
