import asyncio
from typing import Optional, Tuple, List
from pydantic import BaseModel
from abc import ABC, abstractmethod
from datetime import time, datetime, timezone, timedelta

from src.config import DEFAULT_TD
from src.tools.safe_dict import SafeDict


class Task(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def __call__(self) -> None: ...


class SchedulerConfig(BaseModel):
    time_config: time
    cycle: bool = True
    interval: bool = False

    def get_timedelta(self):
        return timedelta(
            hours=self.time_config.hour,
            minutes=self.time_config.minute,
        )


SCHEDULE_DICT_T = SafeDict[time, List[Tuple[SchedulerConfig, Task]]]


class Scheduler:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        if not loop:
            loop = asyncio.get_event_loop()

        self.loop = loop
        self.schedule: SCHEDULE_DICT_T = SafeDict()

        self.loop.create_task(self.__loop())

    def nowtime(self):
        return datetime.now(timezone.utc) + DEFAULT_TD

    async def create_task(
        self,
        task: Task,
        hours: int = 0,
        minutes: int = 0,
        cycle = True,
        interval = False
    ):
        assert hours != 0 or minutes != 0

        time_info = time(hour=hours, minute=minutes)
        config = SchedulerConfig(time_config=time_info, cycle=cycle, interval=interval)

        if interval:
            dt_config = self.nowtime() + config.get_timedelta()
            time_info = time(dt_config.hour, dt_config.minute)

        schedule_data = await self.schedule.get(time_info) or []

        new_task = (config, task)
        schedule_data.append(new_task)
        await self.schedule.set(time_info, schedule_data)

    async def __loop(self):
        while True:
            now = self.nowtime()
            now_time = time(now.hour, now.minute)

            functions = await self.schedule.get(now_time)
            if not functions:
                continue

            await self.schedule.delete(now_time)

            for func_conf in functions:
                config, func = func_conf
                await func()

                if config.cycle:
                    await asyncio.sleep(65)

                    await self.create_task(
                        task=func,
                        hours=config.time_config.hour,
                        minutes=config.time_config.minute,
                        cycle=config.cycle,
                        interval=config.interval,
                    )
            
            await asyncio.sleep(30)
