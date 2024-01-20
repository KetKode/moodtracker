from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_en import COMMANDS


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description) for command, description in COMMANDS.items()
        ]
    await bot.set_my_commands(main_menu_commands)
