import asyncio
from aiogram import Bot
from datetime import datetime, timezone

from src import texts
from src.config import DEFAULT_TD
from src.database.repositories import UserRepository
from src.database.models import User
from src.tools.safe_dict import SafeDict
from src.tools.group_schedule import get_group_schedule, list_to_text
from src.scheduler import Scheduler, Task


class EverydayAlert(Task):
    def __init__(self, bot: Bot, user: User, cache: SafeDict):
        self.bot = bot
        self.user = user
        self.cache = cache

    async def __call__(self):
        schedule = await get_group_schedule(self.cache, self.user.group)

        now_time = datetime.now(timezone.utc) + DEFAULT_TD
        weekday = now_time.weekday()

        if weekday == 6:
            return
        
        schedule_today = schedule[weekday]
        schedule_text = texts.EVERYDAY_SUB_START + list_to_text(schedule_today)

        await self.bot.send_message(self.user.id, schedule_text)


async def schedule_notifications(bot: Bot, cache: SafeDict):
    enable_notifications_users = await UserRepository.get_all_notifications()
    if not enable_notifications_users:
        return
    
    loop = asyncio.get_event_loop()
    scheduler = Scheduler(loop)

    for user in enable_notifications_users:
        if user.settings.everyday_schedule_alert:
            task = EverydayAlert(bot, user, cache)
            await scheduler.create_task(task, hours=1)

        if user.settings.free_after_classes_alert:
            pass


    
