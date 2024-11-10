from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from loguru import logger

from src.handlers import routers
from src.config import TG_TOKEN, DEFAULT_CACHE
from src.scheduler import Scheduler
from src.tools.safe_dict import SafeDict
from src.middlewares import CacheMiddleware, LoggingMiddleware
from src.scheduler.notifications import schedule_notifications


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    data = dispatcher.workflow_data
    await schedule_notifications(bot, **data)
    
    commands = [
        BotCommand(command="/week", description="Расписание на неделю"),
        BotCommand(command="/chat_free", description="Свободные пользователи из текущего чата"),
        BotCommand(command="/share", description="Позволить другим видеть свое расписание"),
        BotCommand(command="/start", description="Выбрать свою группу"),
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
dp["safe_cache"] = SafeDict(DEFAULT_CACHE)
dp["scheduler"] = Scheduler()

bot = Bot(TG_TOKEN)

dp.startup.register(on_startup)
dp.include_routers(*routers)

dp.update.outer_middleware(LoggingMiddleware())
dp.message.outer_middleware(CacheMiddleware())
dp.callback_query.outer_middleware(CacheMiddleware())
