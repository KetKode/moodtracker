from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_en import LEXICON_EN, emotions_dict

# build starting keyboard - invite to log mood or to refuse
button_log = KeyboardButton(text=LEXICON_EN['log_button'])
button_refuse = KeyboardButton(text=LEXICON_EN['refuse_button'])

start_kb_builder = ReplyKeyboardBuilder()
start_kb_builder.row(button_log)
start_kb_builder.row(button_refuse)

start_kb = start_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# build basic mood types keyboard
button_happy = KeyboardButton(text=emotions_dict["happy"]["label"])
button_sad = KeyboardButton(text=emotions_dict["sad"]["label"])
button_angry = KeyboardButton(text=emotions_dict["angry"]["label"])
button_surprised = KeyboardButton(text=emotions_dict["surprised"]["label"])
button_fearful = KeyboardButton(text=emotions_dict["fearful"]["label"])
button_bad = KeyboardButton(text=emotions_dict["bad"]["label"])
button_disgusted = KeyboardButton(text=emotions_dict["disgusted"]["label"])

basic_emotions_buttons = [button_happy, button_sad, button_angry, button_surprised,
                          button_fearful, button_bad, button_disgusted]

basic_emotions_kb_builder = ReplyKeyboardBuilder()
basic_emotions_kb_builder.row(*basic_emotions_buttons, width=3)

basic_emotions_kb = basic_emotions_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** happy **

sub_emotions_happy_kb_builder = ReplyKeyboardBuilder()
sub_emotions_happy_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["happy"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_happy_buttons.append(button)

sub_emotions_happy_kb_builder.row(*sub_emotions_happy_buttons, width=3)


sub_emotions_happy_kb = sub_emotions_happy_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** sad **

sub_emotions_sad_kb_builder = ReplyKeyboardBuilder()
sub_emotions_sad_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["sad"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_sad_buttons.append(button)

sub_emotions_sad_kb_builder.row(*sub_emotions_sad_buttons, width=3)


sub_emotions_sad_kb = sub_emotions_sad_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** angry **

sub_emotions_angry_kb_builder = ReplyKeyboardBuilder()
sub_emotions_angry_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["angry"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_angry_buttons.append(button)

sub_emotions_angry_kb_builder.row(*sub_emotions_angry_buttons, width=3)


sub_emotions_angry_kb = sub_emotions_angry_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** surprised **

sub_emotions_surprised_kb_builder = ReplyKeyboardBuilder()
sub_emotions_surprised_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["surprised"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_surprised_buttons.append(button)

sub_emotions_surprised_kb_builder.row(*sub_emotions_surprised_buttons, width=3)


sub_emotions_surprised_kb = sub_emotions_surprised_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** fearful **

sub_emotions_fearful_kb_builder = ReplyKeyboardBuilder()
sub_emotions_fearful_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["fearful"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_fearful_buttons.append(button)

sub_emotions_fearful_kb_builder.row(*sub_emotions_fearful_buttons, width=3)


sub_emotions_fearful_kb = sub_emotions_fearful_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** bad **

sub_emotions_bad_kb_builder = ReplyKeyboardBuilder()
sub_emotions_bad_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["bad"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_bad_buttons.append(button)

sub_emotions_bad_kb_builder.row(*sub_emotions_bad_buttons, width=3)


sub_emotions_bad_kb = sub_emotions_bad_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )

# builder deeper shades of emotions keyboard for ** disgusted **

sub_emotions_disgusted_kb_builder = ReplyKeyboardBuilder()
sub_emotions_disgusted_buttons = []
for sub_emotion_key, sub_emotion_value in emotions_dict["disgusted"]["sub_emotions"].items():
    button = KeyboardButton(text=sub_emotion_value["label"])
    sub_emotions_disgusted_buttons.append(button)

sub_emotions_disgusted_kb_builder.row(*sub_emotions_disgusted_buttons, width=3)


sub_emotions_disgusted_kb = sub_emotions_disgusted_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )