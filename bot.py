import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers

# initialize the logger
logger = logging.getLogger(__name__)

config = load_config()

# initialize bot and dispatcher
bot = Bot(token=config.tg_bot.token,
           parse_mode="HTML")
dp = Dispatcher()


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

    # register routers in dispatcher
    dp.include_router(user_handlers.router)

    # launch polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/help",
                   description="Get available functionality"),
        BotCommand(command="/log",
                   description="Log today's mood"),
        BotCommand(command="/history",
                   description="View your mood history"),
        BotCommand(command="/insights",
                   description="Mood patterns and predictions"),
        BotCommand(command="/tips",
                   description="Get tips to deal with current mood")

        ]
    await bot.set_my_commands(main_menu_commands)

if __name__ == "__main__":
    dp.startup.register(set_main_menu)
    asyncio.run(main())
