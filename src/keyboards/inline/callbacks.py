from aiogram.filters.callback_data import CallbackData


class EverydayScheduleCallback(CallbackData, prefix="everyday_schedule"):
    """
    Update everyday schedule notification status callback
    """


class AfterClassesCallback(CallbackData, prefix="after_classes"):
    """
    Update after classes notification status callback
    """


class UpdateShareCallback(CallbackData, prefix="update_share"):
    """
    Update share status callback
    """
