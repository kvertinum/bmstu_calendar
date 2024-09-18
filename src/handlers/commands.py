from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from typing import Dict, List

from src import texts
from src.tools import SafeDict
from src.parser import SCHEDULE_T, get_group_schedule, list_to_text
from src.handlers.states import UserInfo
from src.database.repositories import UserRepository


router = Router(name="commands-router")


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(UserInfo.group)
    await message.answer(texts.WELCOME_MESSAGE)


@router.message(Command("week"))
async def week_cmd(message: Message, safe_cache: SafeDict):
    user = await UserRepository(message.from_user.id).get()

    schedules: Dict[str, SCHEDULE_T] = await safe_cache.get("schedules")

    group_schedule = schedules.get(user.group)
    if not group_schedule:
        group_schedule = await get_group_schedule(user.group)
        if not group_schedule:
            return await message.answer(texts.GROUP_NOT_EXISTS)
        
        schedules[user.group] = group_schedule
        await safe_cache.set("schedules", schedules)

    res_schedule = ""
    for day in group_schedule:
        res_schedule += list_to_text(day) + "\n"

    return await message.answer(res_schedule)


@router.message(Command("share"))
async def share_cmd(message: Message):
    user_rep = UserRepository(message.from_user.id)
    user = await user_rep.get()

    share_status = not user.share
    await user_rep.update(share=share_status)

    await message.answer(texts.SHARE_STATUS[share_status])
