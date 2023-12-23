import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

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

    # configure Menu button
    await set_main_menu(bot)

    # launch polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
