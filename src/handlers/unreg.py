from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src import texts
from src.handlers.states import UserInfo


router = Router(name="register-router")


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(UserInfo.group)
    await message.answer(texts.WELCOME_MESSAGE)
