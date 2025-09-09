from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from lexicon.lexicon import LEXICON_RU
from keyboards.user import keyboard_1, keyboard_2, keyboard_3
from functions.user import opponents_option, check_user, get_result, get_statistics
from database.database import data

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}!\n\n{LEXICON_RU['/start']}',
                         reply_markup=keyboard_1)

@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'] + '\n\n' + LEXICON_RU['question_1'],
                         reply_markup=keyboard_1)

@router.message(F.text == LEXICON_RU['yes_button'])
async def process_start_command(message: Message):
    check_user(message)
    await message.answer(text=f'{LEXICON_RU['new_game']}',
                         reply_markup=keyboard_2)

@router.message(F.text == LEXICON_RU['no_button'])
async def process_start_command(message: Message):
    await message.answer(text=f'{LEXICON_RU['exit']}')

@router.message(F.text.in_([LEXICON_RU['rock'], LEXICON_RU['scissors'], LEXICON_RU['paper']]))
async def process_help_command(message: Message):
    opponent_choice = opponents_option(message)
    await message.answer(text=f'{LEXICON_RU['bot_choice']} - {LEXICON_RU[opponent_choice]}')
    res = get_result(message, opponent_choice)
    if res == "user_won":
        message_effect_id = "5046509860389126442"
    else:
        message_effect_id = None
    await message.answer(text=LEXICON_RU[res] + '\n\n' + LEXICON_RU['question_2'],
                         message_effect_id=message_effect_id,
                         reply_markup=keyboard_3)

@router.message(F.text == 'СТАТИСТИКА')
async def process_help_command(message: Message):
    await message.answer(text=get_statistics(message) + '\n\n' + LEXICON_RU['question_1'],
                         reply_markup=keyboard_1)

