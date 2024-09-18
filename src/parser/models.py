from typing import Optional
from pydantic import BaseModel, ConfigDict


periods = [
    "08:30 - 10:05",
    "10:15 - 11:50",
    "12:00 - 13:35",
    "13:50 - 15:25",
    "15:40 - 17:15",
    "17:25 - 19:00",
    "19:10 - 20:45",
]


class Class(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    location: str
    time: int
    week: str = "all"

    def __str__(self):
        time = periods[self.time - 1]
        return f"{time} {self.name} ({self.location})" + (
            f" [{self.week}]" if self.week != "all" else ""
        )
