from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram.types import ReplyKeyboardRemove

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'],
                         reply_markup=ReplyKeyboardRemove())