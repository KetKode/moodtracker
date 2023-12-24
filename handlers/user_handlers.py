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
    fearful_sub_moods, bad_sub_moods, disgusted_sub_moods, get_or_create_user
from moodtracker.models.models import User, Mood
from moodtracker.bot import session

router = Router()


class ChooseMood(StatesGroup):
    choosing_action = State()
    choosing_basic_mood = State()
    choosing_sub_mood = State()


# handle start command
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user = get_or_create_user(message.from_user.id, message.from_user.username)
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


# 1 handle choosing **happy** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "happy_pressed")
async def process_happy_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_happy_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 1 handle choosing sub_mood for **happy**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in happy_sub_moods]))
async def process_happy_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 2 handle choosing **sad** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "sad_pressed")
async def process_sad_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_sad_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 2 handle choosing sub_mood for **sad**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in sad_sub_moods]))
async def process_sad_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 3 handle choosing **angry** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "angry_pressed")
async def process_angry_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_angry_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 3 handle choosing sub_mood for **angry**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in angry_sub_moods]))
async def process_angry_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 4 handle choosing **surprised** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "surprised_pressed")
async def process_surprised_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_surprised_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 4 handle choosing sub_mood for **surprised**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in surprised_sub_moods]))
async def process_surprised_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 5 handle choosing **fearful** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "fearful_pressed")
async def process_fearful_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_fearful_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 5 handle choosing sub_mood for **fearful**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in fearful_sub_moods]))
async def process_fearful_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 6 handle choosing **bad** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "bad_pressed")
async def process_bad_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_bad_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 6 handle choosing sub_mood for **bad**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in bad_sub_moods]))
async def process_bad_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


# 7 handle choosing **disgusted** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "disgusted_pressed")
async def process_disgusted_basic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_disgusted_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 7 handle choosing sub_mood for **disgusted**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in disgusted_sub_moods]))
async def process_disgusted_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()
