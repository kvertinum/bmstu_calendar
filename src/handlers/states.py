from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.database.repositories import UserRepository
from src.keyboards.reply import MenuButtons
from src import texts


router = Router(name="state-router")


class UserInfo(StatesGroup):
    group = State()


@router.message(UserInfo.group)
async def select_skills(message: Message, state: FSMContext):
    group = message.text.upper()
    await UserRepository(message.from_user.id).new(group)

    await message.answer(texts.GROUP_SAVED, reply_markup=MenuButtons.menu())

    await state.clear()
