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


ip = os.getenv("ip")
POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
