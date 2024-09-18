import time
from collections.abc import Awaitable, Callable
from typing import Any, cast
from loguru import logger

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update


HANDLED_STR = ["Unhandled", "Handled"]


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event = cast(Update, event)
        _started_processing_at = time.time()

        upd_logger = logger.bind(update_id=event.update_id)

        if event.message:
            message = event.message
            upd_logger = upd_logger.bind(
                message_id=message.message_id,
                chat_type=message.chat.type,
                chat_id=message.chat.id,
            )
            
            if message.from_user is not None:
                upd_logger = upd_logger.bind(user_id=message.from_user.id)

            if message.text:
                upd_logger = upd_logger.bind(text=message.text, entities=message.entities)

            if message.video:
                upd_logger = upd_logger.bind(
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                    video_id=message.video.file_id,
                    video_unique_id=message.video.file_unique_id,
                )

            if message.photo:
                upd_logger = upd_logger.bind(
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                    photo_id=message.photo[-1].file_id,
                    photo_unique_id=message.photo[-1].file_unique_id,
                )
            upd_logger.debug("Received message")

        elif event.callback_query:
            c = event.callback_query
            upd_logger = upd_logger.bind(
                callback_query_id=c.id,
                callback_data=c.data,
                user_id=c.from_user.id,
                inline_message_id=c.inline_message_id,
                chat_instance=c.chat_instance,
            )

            if c.message is not None:
                upd_logger = upd_logger.bind(
                    message_id=c.message.message_id,
                    chat_type=c.message.chat.type,
                    chat_id=c.message.chat.id,
                )
            upd_logger.debug("Received callback query")

        elif event.inline_query:
            query = event.inline_query
            upd_logger = upd_logger.bind(
                query_id=query.id,
                user_id=query.from_user.id,
                query=query.query,
                offset=query.offset,
                chat_type=query.chat_type,
                location=query.location,
            )
            upd_logger.debug("Received inline query")

        elif event.my_chat_member:
            upd = event.my_chat_member
            upd_logger = logger.bind(
                user_id=upd.from_user.id,
                chat_id=upd.chat.id,
                old_state=upd.old_chat_member,
                new_state=upd.new_chat_member,
            )
            upd_logger.debug("Received my chat member update")

        elif event.chat_member:
            upd = event.chat_member
            upd_logger = upd_logger.bind(
                user_id=upd.from_user.id,
                chat_id=upd.chat.id,
                old_state=upd.old_chat_member,
                new_state=upd.new_chat_member,
            )
            upd_logger.debug("Received chat member update")

        await handler(event, data)

        upd_logger = upd_logger.bind(
            process_result=True,
            spent_time_ms=round((time.time() - _started_processing_at) * 10000) / 10,
        )

        if event.message:
            upd_logger.info("Handled message")
        elif event.callback_query:
            upd_logger.info("Handled callback query")
        elif event.inline_query:
            upd_logger.info("Handled inline query")
        elif event.my_chat_member:
            upd_logger.info("Handled my chat member update")
        elif event.chat_member:
            upd_logger.info("Handled chat member update")

        return