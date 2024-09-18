from src.app import dp, bot, logger


if __name__ == "__main__":
    logger.info("starting bot")
    dp.run_polling(bot)
