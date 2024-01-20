from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery

from bot import session
from keyboards.keyboards import basic_emotions_kb, sub_moods_happy_kb, sub_moods_fearful_kb, \
    sub_moods_disgusted_kb, sub_moods_surprised_kb, sub_moods_bad_kb, sub_moods_angry_kb, \
    sub_moods_sad_kb, day_types_kb
from lexicon.lexicon_en import LEXICON_EN, moods_dict, day_types
from models.models import Mood
from services.services import post_a_pixel
from utils.utils import happy_sub_moods, sad_sub_moods, angry_sub_moods, surprised_sub_moods, \
    fearful_sub_moods, bad_sub_moods, disgusted_sub_moods, get_or_create_user

router = Router()


class ChooseMood(StatesGroup):
    choosing_action = State()
    choosing_day_type = State()
    choosing_basic_mood = State()
    choosing_sub_mood = State()
    leaving_note = State()


# handle start command
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user = get_or_create_user(telegram_user_id=message.from_user.id, username=message.from_user.username)

    graph_url = f"https://pixe.la/v1/users/{user.username}/graphs/moodgraph1.html"

    # log or refuse logging - starting keyboard
    log_button = InlineKeyboardButton(text=LEXICON_EN["log_button"], callback_data="log_callback")
    refuse_button = InlineKeyboardButton(text=LEXICON_EN["refuse_button"], callback_data="refuse_callback")

    # an inline button with the dynamically generated URL for the mood graph
    graph_button = InlineKeyboardButton(text="See my mood journal 📓", url=graph_url)
    start_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [log_button],
            [refuse_button],
            [graph_button]
            ]
        )
    await message.answer(text=f"{LEXICON_EN['/start']}\n\n", reply_markup=start_kb)
    await state.set_state(ChooseMood.choosing_action)


# handle graph command - return a link to the user with a graph
@router.message(Command(commands=["graph"]))
async def process_graph_command(message: Message):
    user = get_or_create_user(telegram_user_id=message.from_user.id, username=message.from_user.username)
    graph_url = f"https://pixe.la/v1/users/{user.username}/graphs/moodgraph1"
    graph_button = InlineKeyboardButton(text="See my mood journal 📓", url=graph_url)

    graph_kb = InlineKeyboardMarkup(inline_keyboard=[[graph_button]])

    await message.answer(text=f"{LEXICON_EN['/graph']}",
                         reply_markup=graph_kb)


# handle help command
@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(text=f"{LEXICON_EN['/help']}")


# handle "log button"
@router.callback_query(
    ChooseMood.choosing_action,
    F.data == "log_callback")
async def process_log_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["start_day_type"],
                                     reply_markup=day_types_kb)
    await state.set_state(ChooseMood.choosing_day_type)


# handle log command
@router.message(Command(commands=["log"]))
async def process_log_command(message: Message, state: FSMContext):
    await message.reply(text=LEXICON_EN["start_day_type"], reply_markup=day_types_kb)
    await state.set_state(ChooseMood.choosing_day_type)


# handle "refuse button"
@router.callback_query(
    ChooseMood.choosing_action,
    F.data == "refuse_callback")
async def process_refuse_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["user_refuse"])
    await state.clear()


# handle choosing day type
@router.callback_query(
    ChooseMood.choosing_day_type,
    F.data.in_([f"{day_type}_pressed" for day_type in day_types])
    )
async def process_day_type_answer(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)

    day_type = next(day_type for day_type in day_types if f"{day_type}_pressed" == callback.data)
    day_mood_quantity = day_types[f"{day_type}"]["quantity"]

    await state.update_data(day_type=day_type, day_mood_quantity=day_mood_quantity)
    await callback.message.answer_photo (
        photo="https://miro.medium.com/v2/resize:fit:1080/1*ieAJuyRI3-iOVOBnJzkEwA.jpeg",
        caption="Use this wheel for mood and sub mood reference")
    await callback.message.edit_text(text=LEXICON_EN["/log"], reply_markup=basic_emotions_kb)
    await state.set_state(ChooseMood.choosing_basic_mood)


# 1 handle choosing **happy** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "happy_pressed")
async def process_happy_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)

    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_happy_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 1 handle choosing sub_mood for **happy**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in happy_sub_moods]))
async def process_happy_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["happy"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in happy_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 2 handle choosing **sad** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "sad_pressed")
async def process_sad_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_sad_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 2 handle choosing sub_mood for **sad**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in sad_sub_moods]))
async def process_sad_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["sad"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in sad_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 3 handle choosing **angry** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "angry_pressed")
async def process_angry_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_angry_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 3 handle choosing sub_mood for **angry**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in angry_sub_moods]))
async def process_angry_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["angry"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in angry_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 4 handle choosing **surprised** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "surprised_pressed")
async def process_surprised_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_surprised_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 4 handle choosing sub_mood for **surprised**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in surprised_sub_moods]))
async def process_surprised_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["surprised"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in surprised_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 5 handle choosing **fearful** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "fearful_pressed")
async def process_fearful_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_fearful_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 5 handle choosing sub_mood for **fearful**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in fearful_sub_moods]))
async def process_fearful_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["fearful"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in fearful_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 6 handle choosing **bad** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "bad_pressed")
async def process_bad_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_bad_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 6 handle choosing sub_mood for **bad**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in bad_sub_moods]))
async def process_bad_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["bad"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in bad_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# 7 handle choosing **disgusted** as a basic emotion
@router.callback_query(
    ChooseMood.choosing_basic_mood,
    F.data == "disgusted_pressed")
async def process_disgusted_basic(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    await callback.message.edit_text(text=LEXICON_EN["specify_emotion"],
                                     reply_markup=sub_moods_disgusted_kb)
    await state.set_state(ChooseMood.choosing_sub_mood)


# 7 handle choosing sub_mood for **disgusted**
@router.callback_query(
    ChooseMood.choosing_sub_mood,
    F.data.in_([f"{sub_mood}_pressed" for sub_mood in disgusted_sub_moods]))
async def process_disgusted_selection(callback: CallbackQuery, state: FSMContext):
    user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
    mood_value = moods_dict["disgusted"]["label"]
    sub_mood_value = next(sub_mood for sub_mood in disgusted_sub_moods if f"{sub_mood}_pressed" == callback.data)

    await state.update_data(mood_value=mood_value, sub_mood_value=sub_mood_value)
    await callback.message.reply(text=LEXICON_EN["note_button"])
    await state.set_state(ChooseMood.leaving_note)


# handle note leaving state
@router.message(
    ChooseMood.leaving_note)
async def process_note_accepted(message: Message, state: FSMContext):
    user = get_or_create_user(telegram_user_id=message.from_user.id, username=message.from_user.username)

    data = await state.get_data()
    day_type = data.get('day_type', '')
    day_mood_quantity = data.get('day_mood_quantity', '')
    mood_value = data.get('mood_value', '')
    sub_mood_value = data.get('sub_mood_value', '')
    note = message.text
    print(note)

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type, note=note)
    post_a_pixel(username=user.username, quantity=day_mood_quantity)

    session.add(new_mood)
    session.commit()

    today_date = datetime.today().strftime("%m/%d/%Y")

    graph_button = InlineKeyboardButton(text="See my mood journal 📓", url=user.pixela_graph_url)
    log_button = InlineKeyboardButton(text=LEXICON_EN["log_button"], callback_data="log_callback")
    end_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [graph_button],
            [log_button]
            ]
        )
    await message.reply(text=f"Thank you for logging your mood!\n"
                             f"Today is <b>{today_date}</b>\n"
                             f"Your day was <b>{day_type}</b>\n"
                             f"You felt <b>{mood_value}</b>\n"
                             f"And also you felt <b>{sub_mood_value}</b>\n"
                             f"What happened today: <b>{note}</b>", reply_markup=end_kb)
    await state.set_state(ChooseMood.choosing_action)


# # handle note refused button
# @router.callback_query(
#     ChooseMood.leaving_note,
#     F.data == "note_refuse_pressed")
# async def process_note_accepted(callback: CallbackQuery, state: FSMContext):
#     user = get_or_create_user(telegram_user_id=callback.from_user.id, username=callback.from_user.username)
#
#     data = await state.get_data()
#     day_type = data.get('day_type', '')
#     day_mood_quantity = data.get('day_mood_quantity', '')
#     mood_value = data.get('mood_value', '')
#     sub_mood_value = data.get('sub_mood_value', '')
#
#     new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
#     post_a_pixel(username=user.username, quantity=day_mood_quantity)
#
#     session.add(new_mood)
#     session.commit()
#
#     graph_button = InlineKeyboardButton(text="See my mood journal 📓", url=user.pixela_graph_url)
#     end_kb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [graph_button]
#             ]
#         )
#     await callback.message.reply(text=f"{LEXICON_EN['note_refuse']}", reply_markup=end_kb)
#     await state.clear()
