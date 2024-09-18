from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from loguru import logger

from src.handlers import routers
from src.config import TG_TOKEN
from src.middlewares import CacheMiddleware, LoggingMiddleware


async def set_my_commands():
    commands = [
        BotCommand(command="/start", description="Выбрать свою группу"),
        BotCommand(command="/week", description="Расписание на неделю"),
        BotCommand(command="/share", description="Позволить другим видеть свое расписание")
    ]
    await bot.set_my_commands(commands)


logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level> | {extra}"
)
logger.add("logs.log", format=logger_format)

dp = Dispatcher()
bot = Bot(TG_TOKEN)

dp.startup.register(set_my_commands)
dp.include_routers(*routers)

dp.update.outer_middleware(LoggingMiddleware())
dp.message.middleware(CacheMiddleware())
dp.callback_query.middleware(CacheMiddleware())
