from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Union, Dict, Any

from src.tools.safe_dict import SafeDict
from src.database.repositories import UserRepository, ChatRepository
from src.middlewares.filter import CHAT_TYPES


DEFAULT_USER_DATA = {
    "chats": []
}


class CacheMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        cache: SafeDict[str, Any] = data["safe_cache"]

        user_data = await cache.get(event.from_user.id) or DEFAULT_USER_DATA.copy()

        user = await UserRepository.get(event.from_user.id)
        data["user"] = user
        data["user_rep"] = UserRepository(user)

        chats_status = user_data["chats"]
        if isinstance(event, Message) and event.chat.type in CHAT_TYPES:
            chat_rep = ChatRepository(event.chat.id)
            data["chat_rep"] = chat_rep

            if event.chat.id not in chats_status:
                chats_status.append(event.chat.id)
                await chat_rep.reg_chat_user(event.from_user.id)

        await cache.set(event.from_user.id, user_data)

        data["user_data"] = user_data

        return await handler(event, data)
