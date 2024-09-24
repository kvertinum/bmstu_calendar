from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from typing import Dict
from loguru import logger

from src import texts
from src.middlewares.filter import UserExists
from src.tools import SafeDict, get_group_schedule, group_status
from src.parser import SCHEDULE_T, list_to_text
from src.keyboards.reply import MenuButtons
from src.keyboards.inline import NotificationsButtons
from src.database.repositories import UserRepository
from src.database.models import User


router = Router(name="commands-router")

router.message.filter(UserExists())
router.callback_query.filter(UserExists())


@router.message(Command("week"))
@router.message(F.text == MenuButtons.SCHEDULE_WEEK)
async def week_cmd(message: Message, safe_cache: SafeDict, user: User):
    # logger.debug(str(user.settings))
    schedules: Dict[str, SCHEDULE_T] = await safe_cache.get("group_schedules")

    group_schedule_ex = schedules.get(user.group)
    if not group_schedule_ex:
        await message.answer("Загрузка расписания...")

    group_schedule = await get_group_schedule(safe_cache, user.group)
    if not group_schedule:
        return await message.answer(texts.GROUP_NOT_EXISTS)

    res_schedule = ""
    for day in group_schedule:
        res_schedule += list_to_text(day) + "\n"

    await message.answer(res_schedule, reply_markup=MenuButtons.menu())


@router.message(Command("share"))
async def share_cmd(message: Message, user_rep: UserRepository):
    share_status = await user_rep.update_share_status()

    await message.answer(texts.SHARE_STATUS[share_status])


@router.message(F.text == MenuButtons.SCHEDULE)
async def schedule_button(message: Message):
    await message.answer(texts.SCHEDULE_BUTTONS, reply_markup=MenuButtons.schedule())


@router.message(F.text == MenuButtons.NOTIFICATIONS)
async def notifications_button(message: Message, user: User):
    buttons = NotificationsButtons.notifications_settings(
        everyday_schedule_status=user.settings.everyday_schedule_alert,
        after_classes_status=user.settings.free_after_classes_alert,
    )

    await message.answer(texts.NOTIFICATIONS_SETTINGS, reply_markup=buttons)


@router.message(F.text == MenuButtons.FREE_STUDENTS)
async def free_students_button(message: Message, safe_cache: SafeDict):
    share_open_users = await UserRepository.get_all_share()

    # texted var to send the download text only once
    result_text, texted = "", False
    schedules: Dict[str, SCHEDULE_T] = await safe_cache.get("group_schedules")

    for user in share_open_users:
        schedule_ex = schedules.get(user.group)
        if not schedule_ex and not texted:
            texted = True
            await message.answer("Загрузка расписания...")

        class_now, class_len, last_str = await group_status(safe_cache, user.group)

        if class_now > class_len:
            result_text += texts.USER_FREE_NOW.format(
                name=user.telegram_name,
                user_id=user.id,
            ) + "\n"

        else:
            result_text += texts.USER_BUSY_NOW.format(
                name=user.telegram_name,
                user_id=user.id,
                class_now=class_now,
                class_len=class_len,
                end_time=last_str
            ) + "\n"

    await message.answer(result_text, parse_mode="MarkdownV2")
