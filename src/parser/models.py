from pydantic import BaseModel, ConfigDict
from datetime import time


periods =  [
    [(8, 30), (10, 5)],
    [(10, 15), (11, 50)],
    [(12, 0), (13, 35)],
    [(13, 50), (15, 25)],
    [(15, 40), (17, 15)],
    [(17, 25), (19, 0)],
    [(19, 10), (20, 45)],
]


class Class(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    location: str
    time: int
    week: str = "all"

    def __str__(self):
        time_object = periods[self.time - 1]
        time_str = " - ".join(f"{p[0]:02}:{p[1]:02}" for p in time_object)
        return f"{time_str} {self.name} ({self.location})" + (
            f" [{self.week}]" if self.week != "all" else ""
        )
    
    def time_as_object(self):
        time_object = periods[self.time - 1]
        class_start = time(*time_object[0])
        class_end = time(*time_object[1])
        
        return class_start, class_end
