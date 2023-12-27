from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from moodtracker.keyboards.keyboards import basic_emotions_kb, sub_moods_happy_kb, sub_moods_fearful_kb,\
    sub_moods_disgusted_kb, sub_moods_surprised_kb, sub_moods_bad_kb, sub_moods_angry_kb, \
    sub_moods_sad_kb, day_types_kb
from moodtracker.lexicon.lexicon_en import LEXICON_EN, moods_dict, day_types
from moodtracker.utils.utils import happy_sub_moods, sad_sub_moods, angry_sub_moods, surprised_sub_moods, \
    fearful_sub_moods, bad_sub_moods, disgusted_sub_moods, get_or_create_user
from moodtracker.models.models import User, Mood
from moodtracker.bot import session
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from moodtracker.services.services import post_a_pixel

router = Router()


class ChooseMood(StatesGroup):
    choosing_action = State()
    choosing_day_type = State()
    choosing_basic_mood = State()
    choosing_sub_mood = State()


# handle start command
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user = get_or_create_user(telegram_user_id=message.from_user.id, username=message.from_user.username)

    graph_url = f"https://pixe.la/v1/users/{user.username}/graphs/moodgraph1"

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
    await message.answer(text=f"{LEXICON_EN['/start']}\n\n"
                              f"<b>here is the link to your mood graph:</b>\n"
                              f"https://pixe.la/v1/users/{user.username}/graphs/moodgraph1", reply_markup=start_kb)
    await state.set_state(ChooseMood.choosing_action)


# handle "log button"
@router.callback_query(
    ChooseMood.choosing_action,
    F.data == "log_callback")
async def process_log_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_EN["start_day_type"],
                                     reply_markup=day_types_kb)
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

    data = await state.get_data()
    day_type = data.get('day_type', '')
    day_mood_quantity = data.get('day_mood_quantity', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)

    post_a_pixel(username=user.username, quantity=day_mood_quantity)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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

    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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
    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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

    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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
    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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
    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()


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
    data = await state.get_data()
    day_type = data.get('day_type', '')

    new_mood = Mood(user=user, mood_value=mood_value, sub_mood_value=sub_mood_value, day_type=day_type)
    session.add(new_mood)
    session.commit()
    await callback.message.reply(text=LEXICON_EN["respond_to_log"])
    await state.clear()
