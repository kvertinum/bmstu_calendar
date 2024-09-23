from typing import List

from src.parser.models import Class


def list_to_text(day: List[List[Class]]):
    res_text = ""
    for lesson in day:
        if not lesson:
            continue
        res_text += " | ".join(str(i) for i in lesson) + "\n"
    return res_text
