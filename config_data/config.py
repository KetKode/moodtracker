import os
from dataclasses import dataclass

from dotenv import load_dotenv
from environs import Env

load_dotenv()


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))


POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_USER = str(os.getenv("POSTGRESQL_USER"))
POSTGRESQL_PASSWORD = str(os.getenv("POSTGRESQL_PASSWORD"))
POSTGRESQL_DBNAME = str(os.getenv("POSTGRESQL_DBNAME"))
