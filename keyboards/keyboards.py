from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import CommandStart

from moodtracker.lexicon.lexicon_en import LEXICON_EN, moods_dict, day_types
from moodtracker.utils.utils import happy_sub_moods, sad_sub_moods, angry_sub_moods, surprised_sub_moods, \
    fearful_sub_moods, bad_sub_moods, disgusted_sub_moods

# start logging - day types

day_types_buttons = []
for day_type in day_types:
    button = InlineKeyboardButton(text=day_type, callback_data=f"{day_type}_pressed")
    day_types_buttons.append([button])

day_types_kb = InlineKeyboardMarkup(inline_keyboard=day_types_buttons)

# log or refuse logging - starting keyboard
log_button = InlineKeyboardButton(text=LEXICON_EN["log_button"],
                                  callback_data="log_callback")
refuse_button = InlineKeyboardButton(text=LEXICON_EN["refuse_button"],
                                     callback_data="refuse_callback")

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [log_button],
        [refuse_button]
        ]
    )

# basic mood types keyboard
button_happy = InlineKeyboardButton(text=moods_dict["happy"]["label"],
                                    callback_data="happy_pressed")
button_sad = InlineKeyboardButton(text=moods_dict["sad"]["label"],
                                  callback_data="sad_pressed")
button_angry = InlineKeyboardButton(text=moods_dict["angry"]["label"],
                                    callback_data="angry_pressed")
button_surprised = InlineKeyboardButton(text=moods_dict["surprised"]["label"],
                                        callback_data="surprised_pressed")
button_fearful = InlineKeyboardButton(text=moods_dict["fearful"]["label"],
                                      callback_data="fearful_pressed")
button_bad = InlineKeyboardButton(text=moods_dict["bad"]["label"],
                                  callback_data="bad_pressed")
button_disgusted = InlineKeyboardButton(text=moods_dict["disgusted"]["label"],
                                        callback_data="disgusted_pressed")

basic_emotions_kb = InlineKeyboardMarkup(inline_keyboard=[
    [button_happy], [button_sad], [button_angry],
    [button_surprised], [button_fearful], [button_bad],
    [button_disgusted]
    ])

# deeper shades of emotions keyboard for ** happy **

sub_moods_happy_buttons = []
for sub_mood in happy_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_happy_buttons.append([button])

sub_moods_happy_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_happy_buttons)

# deeper shades of emotions keyboard for ** sad **

sub_moods_sad_buttons = []
for sub_mood in sad_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_sad_buttons.append([button])

sub_moods_sad_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_sad_buttons)

# deeper shades of emotions keyboard for ** angry **

sub_moods_angry_buttons = []
for sub_mood in angry_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_angry_buttons.append([button])

sub_moods_angry_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_angry_buttons)

# deeper shades of emotions keyboard for ** surprised **

sub_moods_surprised_buttons = []
for sub_mood in surprised_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_surprised_buttons.append([button])

sub_moods_surprised_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_surprised_buttons)

# deeper shades of emotions keyboard for ** fearful **

sub_moods_fearful_buttons = []
for sub_mood in fearful_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_fearful_buttons.append([button])

sub_moods_fearful_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_fearful_buttons)

# deeper shades of emotions keyboard for ** bad **

sub_moods_bad_buttons = []
for sub_mood in bad_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_bad_buttons.append([button])

sub_moods_bad_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_bad_buttons)

# deeper shades of emotions keyboard for ** disgusted **

sub_moods_disgusted_buttons = []
for sub_mood in disgusted_sub_moods:
    button = InlineKeyboardButton(text=sub_mood, callback_data=f"{sub_mood}_pressed")
    sub_moods_disgusted_buttons.append([button])

sub_moods_disgusted_kb = InlineKeyboardMarkup(inline_keyboard=sub_moods_disgusted_buttons)
