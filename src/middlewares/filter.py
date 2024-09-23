from aiogram.filters import Filter

from src.database.models import User


class UserExists(Filter):
    async def __call__(self, _, user: User) -> bool:
        return user is not None

