from typing import Dict
from aiogram import Router, Bot
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import (
    Command,
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
)

from src import texts
from src.parser import SCHEDULE_T
from src.middlewares.filter import UserExists, ChatFilter
from src.tools.group_schedule import busy_users_text
from src.tools.safe_dict import SafeDict
from src.database.repositories import ChatRepository, UserRepository


router = Router(name="chats-router")
router.message.filter(UserExists(), ChatFilter())


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def event_new_chat(event: ChatMemberUpdated):
    await event.bot.send_message(event.chat.id, texts.WELCOME_CHAT)


@router.message(Command("chat_free"))
async def chat_free_cmd(
    message: Message,
    chat_rep: ChatRepository,
    safe_cache: SafeDict,
):
    chat_users = await chat_rep.get_chat_users()
    share_open_users = await UserRepository.get_share_by_ids(chat_users)

    undited_message = await message.answer("Загрузка расписания...")

    result_text = await busy_users_text(share_open_users, safe_cache)

    await undited_message.edit_text(result_text, parse_mode="MarkdownV2")
