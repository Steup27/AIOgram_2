import logging
import os
from copy import deepcopy
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


# Функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    end = start + page_size
    error_symbols = ',.!:;?'
    mn = min(end - 1, len(text) - 1)
    if mn == len(text) - 1 and text[-1] in error_symbols:
        return text[start:], len(text[start:])
    for i in range(mn, start - 1, -1):
        if text[i] in error_symbols and text[i + 1] in (' ', '\n'):
            return text[start:i + 1], i + 1 - start
    return '', 0


# Функция, формирующая словарь книги
def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    dict = {}
    with open(path, encoding='utf-8') as f:
        text = f.read()
        start = 0
        cur_str = 1
        while start < len(text) - 1:
            str_text, l = _get_part_text(text, start, page_size)
            dict[cur_str] = str_text.lstrip()
            cur_str += 1
            start += l
        return dict

def get_pagination_keyboard_args(current_page, book) -> list[str]:
    keyboard_args = [f"{current_page}/{len(book)}"]
    if current_page > 1:
        keyboard_args.insert(0, 'backward')
    if current_page < len(book):
        keyboard_args.append('forward')
    keyboard_args.extend(['go_to_the_start', 'go_to_the_end'])
    return keyboard_args

