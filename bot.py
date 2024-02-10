import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config_data.config import load_config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu
from config_data.config import POSTGRESQL_HOST, POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_DBNAME

DATABASE_URL = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DBNAME}"

# define SQLAlchemy model for storing data
Base = declarative_base()

# initialize the logger
logger = logging.getLogger(__name__)

# create SQLAlchemy engine and tables
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# set up Redis storage for FSMContext
redis = Redis(host="localhost")
storage = RedisStorage(redis=redis)


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
    dp = Dispatcher(storage=storage)

    # register routers in dispatcher
    dp.include_router(user_handlers.router)

    # configure Menu button
    await set_main_menu(bot)

    # launch polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
