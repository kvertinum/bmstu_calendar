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
async def select_skills(message: Message, state: FSMContext, user_rep: UserRepository):
    group = message.text.upper()
    name = message.from_user.full_name
    user_id = message.from_user.id
    
    await user_rep.new(
        user_id=user_id,
        group=group,
        tg_name=name,
    )

    await message.answer(texts.GROUP_SAVED, reply_markup=MenuButtons.menu())

    await state.clear()
