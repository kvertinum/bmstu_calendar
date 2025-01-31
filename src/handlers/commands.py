from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from typing import Dict
from datetime import datetime, timedelta, timezone

from src import texts
from src.middlewares.filter import UserExists, PrivateFilter
from src.tools.safe_dict import SafeDict
from src.tools.group_schedule import get_group_schedule, busy_users_text, list_to_text
from src.parser import SCHEDULE_T
from src.keyboards.reply import MenuButtons
from src.keyboards.inline import NotificationsButtons, SettingsButtons
from src.keyboards.inline.callbacks import UpdateShareCallback
from src.database.repositories import UserRepository
from src.database.models import User


router = Router(name="commands-router")

router.message.filter(UserExists(), PrivateFilter())
router.callback_query.filter(UserExists())


@router.message(Command("week"))
@router.message(F.text == MenuButtons.SCHEDULE_WEEK)
async def week_cmd(message: Message, safe_cache: SafeDict, user: User):
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


@router.message(F.text == MenuButtons.SCHEDULE_TODAY)
async def schedule_today(message: Message, safe_cache: SafeDict, user: User):
    schedules: Dict[str, SCHEDULE_T] = await safe_cache.get("group_schedules")

    group_schedule_ex = schedules.get(user.group)
    if not group_schedule_ex:
        await message.answer("Загрузка расписания...")

    group_schedule = await get_group_schedule(safe_cache, user.group)
    if not group_schedule:
        return await message.answer(texts.GROUP_NOT_EXISTS)
    
    tz_settings = timezone(timedelta(hours=3))
    day = datetime.now(tz_settings).weekday()

    res_schedule = "Сегодня нет пар"
    if day < 6:
        res_schedule = list_to_text(group_schedule[day])

    await message.answer(res_schedule, reply_markup=MenuButtons.menu())


@router.message(Command("share"))
async def share_cmd(message: Message, user_rep: UserRepository):
    settings = await user_rep.update_settings(UpdateShareCallback.__prefix__)

    await message.answer(texts.SHARE_STATUS[settings.share])


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


@router.message(F.text == MenuButtons.SETTINGS)
async def settings_button(message: Message, user: User):
    buttons = SettingsButtons.main_settings(
        share_status=user.settings.share,
    )

    await message.answer(texts.MAIN_SETTINGS, reply_markup=buttons)


@router.message(F.text == MenuButtons.FREE_STUDENTS)
async def free_students_button(message: Message, safe_cache: SafeDict):
    share_open_users = await UserRepository.get_all_share()

    undited_message = await message.answer("Загрузка расписания...")

    result_text = await busy_users_text(share_open_users, safe_cache)

    await undited_message.edit_text(result_text, parse_mode="MarkdownV2")
