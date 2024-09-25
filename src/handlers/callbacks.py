from aiogram import Router, Bot
from aiogram.filters import or_f
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from src.database.repositories import UserRepository
from src.keyboards.inline import NotificationsButtons, SettingsButtons


router = Router(name="callbacks-router")


@router.callback_query(or_f(*NotificationsButtons.CALLBACK_FILTERS))
async def notifications_callback(
    cbq: CallbackQuery,
    callback_data: CallbackData,
    bot: Bot,
    user_rep: UserRepository
):
    settings = await user_rep.update_notifications(callback_data.__prefix__)

    buttons = NotificationsButtons.notifications_settings(
        everyday_schedule_status=settings.everyday_schedule_alert,
        after_classes_status=settings.free_after_classes_alert,
    )
    
    await bot.edit_message_reply_markup(
        chat_id=cbq.from_user.id,
        message_id=cbq.message.message_id,
        reply_markup=buttons,
    )

    await cbq.answer()


@router.callback_query(or_f(*SettingsButtons.CALLBACK_FILTERS))
async def settings_callback(
    cbq: CallbackQuery,
    callback_data: CallbackData,
    bot: Bot,
    user_rep: UserRepository
):
    settings = await user_rep.update_settings(callback_data.__prefix__)

    buttons = SettingsButtons.main_settings(
        share_status=settings.share,
    )

    await bot.edit_message_reply_markup(
        chat_id=cbq.from_user.id,
        message_id=cbq.message.message_id,
        reply_markup=buttons,
    )

    await cbq.answer()
