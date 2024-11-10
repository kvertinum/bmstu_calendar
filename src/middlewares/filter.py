from aiogram import types
from aiogram.types import Message
from aiogram.filters import Filter

from src.database.models import User


CHAT_TYPES = ("group", "supergroup")


class UserExists(Filter):
    async def __call__(self, _, user: User) -> bool:
        return user is not None


class ChatFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in CHAT_TYPES
    

class PrivateFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"
