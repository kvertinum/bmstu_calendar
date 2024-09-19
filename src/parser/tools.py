from typing import List
import aiohttp

from src.parser.models import Class
from src.parser.online_parser import OnlineParser
from src.tools import SafeDict


def list_to_text(day: List[List[Class]]):
    res_text = ""
    for lesson in day:
        if not lesson:
            continue
        res_text += " | ".join(str(i) for i in lesson) + "\n"
    return res_text


async def get_group_schedule(cache: SafeDict, group: str):
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
        return group_schedule
