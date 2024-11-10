import aiohttp
from typing import List, Dict, Tuple
from datetime import time, datetime, timezone

from src import texts
from src.tools.safe_dict import SafeDict
from src.database.models import User
from src.parser import OnlineParser, periods, SCHEDULE_T
from src.parser.models import Class
from src.config import DEFAULT_TD


periods_t = [[time(*p[0]), time(*p[1])] for p in periods]


def list_to_text(day: List[List[Class]]):
    res_text = ""
    for lessons in day:
        if not lessons:
            continue
        res_text += " | ".join(str(lesson) for lesson in lessons) + "\n"
    return res_text


async def get_group_schedule(cache: SafeDict, group: str) -> SCHEDULE_T | None:
    group_schedules: Dict[str, SCHEDULE_T] = await cache.get("group_schedules")
    group_schedule = group_schedules.get(group)
    if group_schedule:
        return group_schedule
    
    async with aiohttp.ClientSession() as session:
        parser = OnlineParser(session)
        group_ids = await cache.get("group_ids")
        if not group_ids:
            group_ids = await parser.get_group_ids()
            await cache.set("group_ids", group_ids)

        group_id = group_ids.get(group)
        if not group_id:
            return None

        group_schedule = await parser.get_group_schedule(group_id)
        
        group_schedules[group] = group_schedule
        await cache.set("group_schedules", group_schedules)

        return group_schedule
    

async def group_status(cache: SafeDict, group: str) -> Tuple[int, int, str]:
    group_schedule = await get_group_schedule(cache, group)

    now_datetime = datetime.now(timezone.utc) + DEFAULT_TD

    now_weekday = now_datetime.weekday()

    if now_weekday == 6:
        return 1, 0, ""

    schedule = [i for i in group_schedule[now_weekday] if i]
    schedule_size = len(schedule)
    
    now_time = now_datetime.time()

    for ind, classes in enumerate(schedule):
        period = classes[0].time - 1
        period_t = periods_t[period]
        if period_t[0] <= now_time <= period_t[1]:
            last = schedule[-1][0].time - 1
            last_time = periods[last][1]
            last_time_str = f"{last_time[0]:02}:{last_time[1]:02}"
            return ind+1, schedule_size, last_time_str
        
    return schedule_size+1, schedule_size, ""

async def busy_users_text(users: List[User], safe_cache: SafeDict):
    result_text, texted = "", False

    for user in users:
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

    return result_text
