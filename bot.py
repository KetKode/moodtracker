import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers

# initialize the logger
logger = logging.getLogger(__name__)


# configure and launch the bot
async def main():
    # configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
        )
    # start bot info
    logger.info("Starting bot")

    config = load_config()

    # initialize bot and dispatcher
    bot = Bot(token=config.tg_bot.token,
              parse_mode="HTML")
    dp = Dispatcher()

    # register routers in dispatcher
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # launch polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "main":
    asyncio.run(main())