from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Union, Dict, Any

from src.tools.safe_dict import SafeDict
from src.database.repositories import UserRepository
from loguru import logger


class CacheMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        cache: SafeDict = data["safe_cache"]

        user_data = await cache.get(event.from_user.id)
        if user_data is None:
            user_data = {}
            await cache.set(event.from_user.id, user_data)

        data["user_data"] = user_data

        user = await UserRepository.get(event.from_user.id)
        data["user"] = user
        data["user_rep"] = UserRepository(user)

        return await handler(event, data)
