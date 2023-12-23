from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import CommandStart

from lexicon.lexicon_en import LEXICON_EN, emotions_dict

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
button_happy = InlineKeyboardButton(text=emotions_dict["happy"]["label"],
                                    callback_data="happy_pressed")
button_sad = InlineKeyboardButton(text=emotions_dict["sad"]["label"],
                                  callback_data="sad_pressed")
button_angry = InlineKeyboardButton(text=emotions_dict["angry"]["label"],
                                    callback_data="angry_pressed")
button_surprised = InlineKeyboardButton(text=emotions_dict["surprised"]["label"],
                                        callback_data="surprised_pressed")
button_fearful = InlineKeyboardButton(text=emotions_dict["fearful"]["label"],
                                      callback_data="fearful_pressed")
button_bad = InlineKeyboardButton(text=emotions_dict["bad"]["label"],
                                  callback_data="bad_pressed")
button_disgusted = InlineKeyboardButton(text=emotions_dict["disgusted"]["label"],
                                        callback_data="disgusted_pressed")

basic_emotions_kb = InlineKeyboardMarkup(inline_keyboard=[
    [button_happy], [button_sad], [button_angry],
    [button_surprised], [button_fearful], [button_bad],
    [button_disgusted]
    ])

# # builder deeper shades of emotions keyboard for ** happy **
#
# sub_emotions_happy_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_happy_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["happy"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_happy_buttons.append(button)
#
# sub_emotions_happy_kb_builder.row(*sub_emotions_happy_buttons, width=3)
#
#
# sub_emotions_happy_kb = sub_emotions_happy_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** sad **
#
# sub_emotions_sad_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_sad_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["sad"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_sad_buttons.append(button)
#
# sub_emotions_sad_kb_builder.row(*sub_emotions_sad_buttons, width=3)
#
#
# sub_emotions_sad_kb = sub_emotions_sad_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** angry **
#
# sub_emotions_angry_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_angry_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["angry"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_angry_buttons.append(button)
#
# sub_emotions_angry_kb_builder.row(*sub_emotions_angry_buttons, width=3)
#
#
# sub_emotions_angry_kb = sub_emotions_angry_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** surprised **
#
# sub_emotions_surprised_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_surprised_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["surprised"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_surprised_buttons.append(button)
#
# sub_emotions_surprised_kb_builder.row(*sub_emotions_surprised_buttons, width=3)
#
#
# sub_emotions_surprised_kb = sub_emotions_surprised_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** fearful **
#
# sub_emotions_fearful_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_fearful_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["fearful"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_fearful_buttons.append(button)
#
# sub_emotions_fearful_kb_builder.row(*sub_emotions_fearful_buttons, width=3)
#
#
# sub_emotions_fearful_kb = sub_emotions_fearful_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** bad **
#
# sub_emotions_bad_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_bad_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["bad"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_bad_buttons.append(button)
#
# sub_emotions_bad_kb_builder.row(*sub_emotions_bad_buttons, width=3)
#
#
# sub_emotions_bad_kb = sub_emotions_bad_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )
#
# # builder deeper shades of emotions keyboard for ** disgusted **
#
# sub_emotions_disgusted_kb_builder = ReplyKeyboardBuilder()
# sub_emotions_disgusted_buttons = []
# for sub_emotion_key, sub_emotion_value in emotions_dict["disgusted"]["sub_emotions"].items():
#     button = KeyboardButton(text=sub_emotion_value["label"])
#     sub_emotions_disgusted_buttons.append(button)
#
# sub_emotions_disgusted_kb_builder.row(*sub_emotions_disgusted_buttons, width=3)
#
#
# sub_emotions_disgusted_kb = sub_emotions_disgusted_kb_builder.as_markup(
#     one_time_keyboard=True,
#     resize_keyboard=True
#     )