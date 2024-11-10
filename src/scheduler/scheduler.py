import asyncio
import uuid
from typing import Optional, Dict
from pydantic import BaseModel
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta

from src.config import DEFAULT_TD


class Task(ABC):
    task_id: Optional[int] = None

    def __init__(self):
        self.task_id = uuid.uuid4()

    @abstractmethod
    async def __call__(self) -> None: ...


class TaskConfig(BaseModel):
    hours: Optional[int]
    minutes: Optional[int]
    cycle: bool
    interval: bool


class Scheduler:
    def __init__(self):
        self.task_configs: Dict[uuid.UUID, TaskConfig] = {}
        self._lock = asyncio.Lock()
    
    def _calc_next_run(self, task_id: int):
        config = self.task_configs[task_id]
        now = datetime.now(timezone.utc) + DEFAULT_TD

        if config.interval:
            hours = config.hours or 0
            minutes = config.minutes or 0
            td = timedelta(hours=hours, minutes=minutes)
        else:
            when = now.replace(
                hour=config.hours,
                minute=config.minutes,
                second=0,
                microsecond=0,
            )

            if when < now:
                when = when.replace(day = when.day+1)

            td = when - now

        return td.total_seconds()
    
    async def _create_task(self, task: Task, delay: int, cycle: bool):
        await asyncio.sleep(delay)
        if task.task_id not in self.task_configs:
            return
        
        await task()

        if cycle:
            new_delay = self._calc_next_run(task.task_id)
            asyncio.create_task(self._create_task(task, new_delay, cycle))

    async def remove_task(self, task_id: int):
        async with self._lock:
            self.task_configs.pop(task_id)

    async def schedule_task(
        self, task: Task,
        hours: Optional[int] = None,
        minutes: Optional[int] = None,
        cycle: bool = True,
        interval: bool = False,
    ):
        async with self._lock:
            assert task.task_id is not None

            self.task_configs[task.task_id] = TaskConfig(
                hours=hours,
                minutes=minutes,
                cycle=cycle,
                interval=interval,
            )

            delay = self._calc_next_run(task.task_id)
            asyncio.create_task(self._create_task(task, delay, cycle))
