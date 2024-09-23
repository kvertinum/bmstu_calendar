import aiohttp
from typing import Dict
from datetime import time, datetime, timezone, timedelta

from src.tools import SafeDict
from src.parser import OnlineParser, periods, SCHEDULE_T


periods_t = [[time(*p[0]), time(*p[1])] for p in periods]


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
    

async def group_status(cache: SafeDict, group: str):
    group_schedule = await get_group_schedule(cache, group)

    now_datetime = datetime.now(timezone.utc) + timedelta(hours=3)

    now_weekday = now_datetime.weekday()

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
