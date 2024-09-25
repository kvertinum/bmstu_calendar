from aiogram.filters.callback_data import CallbackQueryFilter
from typing import List

from src.keyboards.inline.const import InlineConstructor
from src.keyboards.inline import callbacks


status_emojis = ["❌", "✅"]


class SettingsButtons(InlineConstructor):
    SHARE_STATUS = "{} Видимость вашего расписания"

    CALLBACK_FILTERS: List[CallbackQueryFilter] = [
        callbacks.UpdateShareCallback.filter(),
    ]


    @classmethod
    def main_settings(
        cls,
        share_status: bool,
    ):
        schema = [1]

        share_status_emoji = status_emojis[share_status]

        buttons = [
            {
                "text": cls.SHARE_STATUS.format(share_status_emoji),
                "callback_data": callbacks.UpdateShareCallback()
            },
        ]

        return cls._create_kb(buttons, schema)
