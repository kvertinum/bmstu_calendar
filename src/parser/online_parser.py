import aiohttp
from typing import Dict, List

from src.config import LIST_API_URL, GROUP_API_URL
from src.parser.models import Class


SCHEDULE_T = List[List[List[Class]]]


class OnlineParser:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_group_ids(self):
        async with self.session.get(LIST_API_URL) as resp:
            resp_json = await resp.json()
            main_building = resp_json["data"]["children"][0]["children"]
            group_ids: Dict[str, str] = {
                group["abbr"]: group["uuid"]
                for faculty in main_building
                for dep in faculty["children"]
                for cource in dep["children"]
                for group in cource["children"]
            }

            return group_ids

    async def get_group_schedule(self, group_id: str):
        res_schedule: SCHEDULE_T = [[[] for _ in range(7)] for _ in range(6)]

        group_url = GROUP_API_URL.format(group_id=group_id)
        async with self.session.get(group_url) as resp:
            resp_json = await resp.json()
            schedule = resp_json["data"]["schedule"]

            for info in schedule:
                day, time = info["day"], info["time"]
                locations = " / ".join(i["name"] for i in info["audiences"])

                curr_class = Class(
                    name=info["discipline"]["fullName"],
                    location=locations,
                    time=time,
                    week=info["week"]
                )

                res_schedule[day - 1][time - 1].append(curr_class)

        return res_schedule
