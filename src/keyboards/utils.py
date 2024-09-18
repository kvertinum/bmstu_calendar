from collections.abc import Sequence
from typing import TypeVar

from src.exceptions.keyboard import WrongKeyboardSchemaError

T = TypeVar("T")


def create_keyboard_layout(buttons: Sequence[T], count: Sequence[int]) -> list[list[T]]:
    if sum(count) != len(buttons):
        raise WrongKeyboardSchemaError(
            schema_size=sum(count),
            buttons_count=len(buttons),
        )
    
    tmplist: list[list[T]] = []
    btn_number = 0
    for line in count:
        tmplist.append([])
        for _ in range(line):
            tmplist[-1].append(buttons[btn_number])
            btn_number += 1
    return tmplist
