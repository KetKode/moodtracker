from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboards import start_kb, basic_emotions_kb, sub_emotions_happy_kb, sub_emotions_sad_kb,\
    sub_emotions_angry_kb, sub_emotions_surprised_kb, sub_emotions_fearful_kb,\
    sub_emotions_bad_kb, sub_emotions_disgusted_kb
from lexicon.lexicon_en import LEXICON_EN, emotions_dict

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_EN["/start"], reply_markup=start_kb)


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_EN["/help"])


@router.message(Command(commands="log"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_EN["/log"], reply_markup=basic_emotions_kb)


@router.message(F.text == LEXICON_EN["log_button"])
async def process_log_request(message: Message):
    await message.reply(text=LEXICON_EN["/log"], reply_markup=basic_emotions_kb)


@router.message(F.text == LEXICON_EN["refuse_button"])
async def process_log_request(message: Message):
    await message.reply(text=LEXICON_EN["user_refuse"])


@router.message(F.text == emotions_dict["happy"]["label"])
async def process_happy_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_happy_kb)


@router.message(F.text == emotions_dict["sad"]["label"])
async def process_sad_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_sad_kb)


@router.message(F.text == emotions_dict["angry"]["label"])
async def process_angry_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_angry_kb)


@router.message(F.text == emotions_dict["surprised"]["label"])
async def process_surprised_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_surprised_kb)


@router.message(F.text == emotions_dict["fearful"]["label"])
async def process_fearful_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_fearful_kb)


@router.message(F.text == emotions_dict["bad"]["label"])
async def process_bad_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_bad_kb)


@router.message(F.text == emotions_dict["disgusted"]["label"])
async def process_disgusted_answer(message: Message):
    await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_disgusted_kb)

