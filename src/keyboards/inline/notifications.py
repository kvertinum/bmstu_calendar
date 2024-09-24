from src.keyboards.inline.const import InlineConstructor
from src.keyboards.inline import callbacks


status_emojis = ["❌", "✅"]


class NotificationsButtons(InlineConstructor):
    EVERYDAY_SCHEDULE = "{} Ежедневное расписание"
    FREE_AFTER_CLASSES = "{} Свободные после пар"


    @classmethod
    def notifications_settings(
        cls,
        everyday_schedule_status: bool,
        after_classes_status: bool,
    ):
        schema = [1, 1]

        everyday_schedule_emoji = status_emojis[everyday_schedule_status]
        after_classes_emoji = status_emojis[after_classes_status]

        buttons = [
            {
                "text": cls.EVERYDAY_SCHEDULE.format(everyday_schedule_emoji),
                "callback_data": callbacks.EverydayScheduleCallback(
                    everyday_schedule=everyday_schedule_status,
                )
            },
            {
                "text": cls.FREE_AFTER_CLASSES.format(after_classes_emoji),
                "callback_data": callbacks.AfterClassesCallback(
                    free_after_classes=after_classes_status,
                )
            },
        ]

        return cls._create_kb(buttons, schema)
