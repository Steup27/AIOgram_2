from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_START_MENU

def create_start_menu() -> InlineKeyboardMarkup:
    keyboard_args = [[InlineKeyboardButton(text=v, callback_data=k)] for k, v in LEXICON_START_MENU.items()]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_args)
    return keyboard