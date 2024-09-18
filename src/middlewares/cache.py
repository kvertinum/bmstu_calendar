from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Union, Dict, Any

from src.tools import SafeDict


DEFAULT_DICT = {"schedules": {}}


class CacheMiddleware(BaseMiddleware):
    def __init__(self):
        self.cache = SafeDict(DEFAULT_DICT)
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_data = await self.cache.get(event.from_user.id)
        if user_data is None:
            user_data = {}
            await self.cache.set(event.from_user.id, user_data)
        data["user_cache"] = user_data
        data["safe_cache"] = self.cache
        return await handler(event, data)