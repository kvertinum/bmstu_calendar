from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from loguru import logger

from src import texts
from src.handlers.states import UserInfo
from src.database.repositories import UserRepository
from src.middlewares.filter import ChatFilter, PrivateFilter


router = Router(name="unreg-router")


@router.message(CommandStart(), PrivateFilter())
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(UserInfo.group)
    await message.answer(texts.WELCOME_MESSAGE)


@router.message(Command("group"), ChatFilter())
async def group_cmd(message: Message, command: CommandObject, user_rep: UserRepository):
    if not command.args:
        return await message.answer(texts.BAD_GROUP_CMD)
    
    command_args = command.args.split()
    group = command_args[0].upper()
    name = message.from_user.full_name
    user_id = message.from_user.id

    await user_rep.new(
        user_id=user_id,
        group=group,
        tg_name=name,
    )

    await message.answer(texts.CHAT_GROUP_SAVED)
