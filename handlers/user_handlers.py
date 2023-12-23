from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from moodtracker.keyboards.keyboards import start_kb, basic_emotions_kb, sub_emotions_happy_kb, sub_emotions_fearful_kb,\
    sub_emotions_disgusted_kb, sub_emotions_surprised_kb, sub_emotions_bad_kb, sub_emotions_angry_kb, \
    sub_emotions_sad_kb
from moodtracker.lexicon.lexicon_en import LEXICON_EN, emotions_dict

router = Router()


class ChooseMood(StatesGroup):
    choosing_basic_mood = State()
    choosing_sub_mood = State()


# handle start command
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_EN["/start"], reply_markup=start_kb)
    await state.set_state(ChooseMood.choosing_basic_mood)


# handle "log button"
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "log_callback")
async def process_log_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["/log"],
                                     reply_markup=basic_emotions_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# handle "refuse button"
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "refuse_callback")
async def process_refuse_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["user_refuse"])


# @router.callback_query(F.data == f"{sub_emotion_value['label']}_pressed")

#
#
# @router.message(Command(commands="help"))
# async def process_help_command(message: Message):
#     await message.answer(text=LEXICON_EN["/help"])
#
#
# @router.message(Command(commands="log"))
# async def process_help_command(message: Message):
#     await message.answer(text=LEXICON_EN["/log"], reply_markup=basic_emotions_kb)
#
#
# @router.message(F.text == LEXICON_EN["log_button"])
# async def process_log_request(message: Message):
#     await message.reply(text=LEXICON_EN["/log"], reply_markup=basic_emotions_kb)
#
#
# @router.message(F.text == LEXICON_EN["refuse_button"])
# async def process_log_request(message: Message):
#     await message.reply(text=LEXICON_EN["user_refuse"])
#
#
# @router.message(F.text == emotions_dict["happy"]["label"])
# async def process_happy_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_happy_kb)
#
#
# @router.message(F.text == emotions_dict["sad"]["label"])
# async def process_sad_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_sad_kb)
#
#
# @router.message(F.text == emotions_dict["angry"]["label"])
# async def process_angry_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_angry_kb)
#
#
# @router.message(F.text == emotions_dict["surprised"]["label"])
# async def process_surprised_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_surprised_kb)
#
#
# @router.message(F.text == emotions_dict["fearful"]["label"])
# async def process_fearful_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_fearful_kb)
#
#
# @router.message(F.text == emotions_dict["bad"]["label"])
# async def process_bad_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_bad_kb)
#
#
# @router.message(F.text == emotions_dict["disgusted"]["label"])
# async def process_disgusted_answer(message: Message):
#     await message.reply(text=LEXICON_EN["specify_emotion"], reply_markup=sub_emotions_disgusted_kb)
#
