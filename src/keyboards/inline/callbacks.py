from aiogram.filters.callback_data import CallbackData


class EverydayScheduleCallback(CallbackData, prefix="everyday_schedule"):
    everyday_schedule: bool

class AfterClassesCallback(CallbackData, prefix="after_classes"):
    free_after_classes: bool
