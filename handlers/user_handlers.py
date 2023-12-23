from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from moodtracker.keyboards.keyboards import start_kb, basic_emotions_kb, sub_moods_happy_kb, sub_moods_fearful_kb,\
    sub_moods_disgusted_kb, sub_moods_surprised_kb, sub_moods_bad_kb, sub_moods_angry_kb, \
    sub_moods_sad_kb
from moodtracker.lexicon.lexicon_en import LEXICON_EN, moods_dict
from moodtracker.utils.utils import happy_sub_moods, sad_sub_moods, angry_sub_moods, surprised_sub_moods, \
    fearful_sub_moods, bad_sub_moods, disgusted_sub_moods

router = Router()


class ChooseMood(StatesGroup):
    choosing_action = State()
    choosing_basic_mood = State()
    choosing_sub_mood = State()


# handle start command
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_EN["/start"], reply_markup=start_kb)
    await state.set_state(ChooseMood.choosing_action)


# handle "log button"
@router.callback_query(
    ChooseMood.choosing_action,
    F.data == "log_callback")
async def process_log_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["/log"],
                                     reply_markup=basic_emotions_kb)
    await state.set_state(ChooseMood.choosing_basic_mood)


# handle "refuse button"
@router.callback_query(
    ChooseMood.choosing_action,
    F.data == "refuse_callback")
async def process_refuse_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["user_refuse"])
    await state.clear()


# handle choosing **happy** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "happy_pressed")
async def process_happy_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_happy_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# handle choosing sub_mood for **happy**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in happy_sub_moods]))
async def process_happy_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# handle choosing **sad** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "sad_pressed")
async def process_sad_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_sad_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# handle choosing sub_mood for **sad**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.text.in_(sad_sub_moods))
async def process_sad_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["respond_to_log"])

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
