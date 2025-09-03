from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

btn_1_1 = KeyboardButton(text=LEXICON_RU['yes_button'])
btn_1_2 = KeyboardButton(text=LEXICON_RU['no_button'])

keyboard_1 = ReplyKeyboardMarkup(
    keyboard=[[btn_1_1, btn_1_2]],
    resize_keyboard=True,
    one_time_keyboard=True
)

btn_2_1 = KeyboardButton(text=LEXICON_RU['rock'])
btn_2_2 = KeyboardButton(text=LEXICON_RU['scissors'])
btn_2_3 = KeyboardButton(text=LEXICON_RU['paper'])

keyboard_2 = ReplyKeyboardMarkup(
    keyboard=[[btn_2_1, btn_2_2, btn_2_3]],
    resize_keyboard=True
)

btn_3_1 = KeyboardButton(text=LEXICON_RU['statistics'])

keyboard_3 = ReplyKeyboardMarkup(
    keyboard=[[btn_1_1, btn_1_2], [btn_3_1]],
    resize_keyboard=True
)




