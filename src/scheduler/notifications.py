from aiogram import Bot
from datetime import datetime, timezone

from src import texts
from src.config import DEFAULT_TD
from src.database.repositories import UserRepository
from src.database.models import User
from src.tools.safe_dict import SafeDict
from src.tools.group_schedule import get_group_schedule, group_status, list_to_text
from src.middlewares.cache import DEFAULT_USER_DATA
from src.scheduler import Scheduler, Task


class EverydayAlert(Task):
    def __init__(self, bot: Bot, user: User, cache: SafeDict):
        self.bot = bot
        self.user = user
        self.cache = cache

        super().__init__()

    async def __call__(self):
        schedule = await get_group_schedule(self.cache, self.user.group)

        now_time = datetime.now(timezone.utc) + DEFAULT_TD
        weekday = now_time.weekday()

        if weekday == 6:
            return
        
        schedule_today = schedule[weekday]
        schedule_text = texts.EVERYDAY_SUB_START + list_to_text(schedule_today)

        await self.bot.send_message(self.user.id, schedule_text)


class AfterClassesAlert(Task):
    def __init__(self, bot: Bot, user: User, cache: SafeDict, weekday: int):
        self.bot = bot
        self.user = user
        self.cache = cache
        self.weekday = weekday

        super().__init__()

    async def __call__(self):
        now_time = datetime.now(timezone.utc) + DEFAULT_TD
        weekday = now_time.weekday()

        if weekday != self.weekday:
            return
        
        share_open_users = await UserRepository.get_all_share()
        result_texts = []

        for user in share_open_users:
            class_now, class_len, _ = await group_status(self.cache, user.group)

            if class_now > class_len:
                result_texts.append(texts.USER_FREE_NOW.format(
                    name=user.telegram_name,
                    user_id=user.id,
                ))

        result_text = "\n".join(result_text)

        if result_text:
            result_text = texts.AFTERCLS_SUB_START + result_text
        else:
            result_text = texts.NO_FREE_USERS

        await self.bot.send_message(self.user.id, result_text, parse_mode="MarkdownV2")


async def setup_aftercls_alert(scheduler: Scheduler, bot: Bot, cache: SafeDict, user: User):
    task_ids = []
    user_schedule = await get_group_schedule(cache, user.group)

    for ind, day in enumerate(user_schedule):
        day = [i for i in day if i]
        if not day:
            continue

        last_class = day[-1][0]
        _, end_time = last_class.time_as_object()
        
        task = AfterClassesAlert(bot, user, cache, ind+1)
        task_ids.append(task.task_id)

        await scheduler.schedule_task(task, end_time.hour, end_time.minute)
    
    return task_ids

async def user_schedule_notifications(user: User, bot: Bot, safe_cache: SafeDict, scheduler: Scheduler):
    user_data = await safe_cache.get(user.id) or DEFAULT_USER_DATA.copy()

    alert_id = user_data.get("everyday_schedule_alert_id")
    alert_status = user.settings.everyday_schedule_alert
    if alert_status != bool(alert_id):
        if alert_status:
            task = EverydayAlert(bot, user, safe_cache)
            await scheduler.schedule_task(task, hours=1, minutes=0)
            user_data["everyday_schedule_alert_id"] = task.task_id
        else:
            user_data.pop("everyday_schedule_alert_id")
            await scheduler.remove_task(alert_id)

    alert_ids = user_data.get("free_after_classes_alert_ids")
    alert_status = user.settings.free_after_classes_alert
    if alert_status != bool(alert_ids):
        if alert_status:
            task_ids = await setup_aftercls_alert(scheduler, bot, safe_cache, user)
            user_data["free_after_classes_alert_ids"] = task_ids
        else:
            user_data.pop("free_after_classes_alert_ids")
            for alert_id in alert_ids:
                await scheduler.remove_task(alert_id)

    await safe_cache.set(user.id, user_data)

async def schedule_notifications(bot: Bot, safe_cache: SafeDict, scheduler: Scheduler):
    enable_notifications_users = await UserRepository.get_all_notifications()

    for user in enable_notifications_users:
        await user_schedule_notifications(user, bot, safe_cache, scheduler)
