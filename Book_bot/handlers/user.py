from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, FSInputFile
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.start_menu import create_start_menu
from lexicon.lexicon import LEXICON
from services.file_handling import get_pagination_keyboard_args
from database.database import JSONDatabase
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

user_router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@user_router.message(CommandStart())
async def process_start_command(message: Message, db: JSONDatabase):
    db.get_user(message.from_user.id)
    await message.answer_photo(photo=FSInputFile('book/cover.png'),
                               caption=LEXICON[message.text],
                               reply_markup=create_start_menu())


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@user_router.message(Command(commands="beginning"))
async def process_beginning_command(message: Message, book: dict, db: JSONDatabase):
    user = db.get_user(message.from_user.id)
    db.update_user_page(user.user_id, 1)
    text = book[1]
    keyboard_args = get_pagination_keyboard_args(1, book)
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
    )


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@user_router.message(Command(commands="continue"))
async def process_continue_command(message: Message, book: dict, db: JSONDatabase):
    user = db.get_user(message.from_user.id)
    text = book[user.current_page]
    keyboard_args = get_pagination_keyboard_args(user.current_page, book)
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
    )


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@user_router.message(Command(commands="bookmarks"))
async def process_bookmarks_command(message: Message, book: dict, db: JSONDatabase):
    user = db.get_user(message.from_user.id)
    if user.bookmarks:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *user.bookmarks, book=book
            ),
        )
    else:
        await message.answer(text=LEXICON["no_bookmarks"])


# Этот хэндлер будет срабатывать на ввод любого целого числа
# и переходить к указанной странице или сообщать, что
# указанной страницы не существует
@user_router.message(F.text.isdigit())
async def process_backward_press(message: Message, book: dict, db: JSONDatabase):
    num = int(message.text)
    if 0 <= num <= len(book):
        text = book[num]
        user = db.get_user(message.from_user.id)
        db.update_user_page(user.user_id, num)
        keyboard_args = get_pagination_keyboard_args(user.current_page, book)
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(*keyboard_args),
        )
    else:
        await message.delete()
        await message.answer(LEXICON['error_page'] + '\n' + f'Введи номер в диапазоне от 1 до {len(book)}')

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@user_router.callback_query(F.data == "start")
async def process_start_command(callback: CallbackQuery, db: JSONDatabase):
    await callback.message.answer_photo(photo=FSInputFile('book/cover.png'),
                               caption=LEXICON['/start'],
                               reply_markup=create_start_menu())

# Этот хэндлер будет срабатывать на нажатие кнопки стартового меню "Начать читать"
@user_router.callback_query(F.data == "start_beginning")
async def process_backward_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    db.update_user_page(user.user_id, 1)
    text = book[1]
    keyboard_args = get_pagination_keyboard_args(user.current_page, book)
    await callback.message.delete()
    await callback.message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
        )

# Этот хэндлер будет срабатывать на нажатие кнопки стартового меню "О книге"
@user_router.callback_query(F.data == "about_book")
async def process_backward_press(callback: CallbackQuery, db: JSONDatabase):
    await callback.message.delete()
    await callback.message.answer(
        text=db.book,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='start')]]),
        )

# Этот хэндлер будет срабатывать на нажатие кнопки стартового меню "Справка"
@user_router.callback_query(F.data == "start_help")
async def process_backward_press(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON['/help'],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='start')]]),
        )

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперёд"
# во время взаимодействия пользователя с сообщением-книгой
@user_router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    current_page = user.current_page
    if current_page < len(book):
        db.update_user_page(user.user_id, current_page + 1)
        text = book[user.current_page]
        keyboard_args = get_pagination_keyboard_args(user.current_page, book)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(*keyboard_args),
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@user_router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    current_page = user.current_page
    if current_page > 1:
        db.update_user_page(user.user_id, current_page - 1)
        text = book[user.current_page]
        keyboard_args = get_pagination_keyboard_args(user.current_page, book)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(*keyboard_args),
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@user_router.callback_query(lambda x: "/" in x.data and x.data.replace("/", "").isdigit())
async def process_page_press(callback: CallbackQuery, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    db.add_bookmark(user.user_id, user.current_page)
    await callback.answer("Страница добавлена в закладки!")


# Этот хэндлер будет срабатывать на нажатие кнопки "Перейти к странице..."
@user_router.callback_query(F.data == "go_to_the_start")
async def process_backward_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    db.update_user_page(user.user_id, 1)
    text = book[1]
    keyboard_args = get_pagination_keyboard_args(user.current_page, book)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
        )

# Этот хэндлер будет срабатывать на нажатие кнопки "Перейти к странице..."
@user_router.callback_query(F.data == "go_to_the_end")
async def process_backward_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    db.update_user_page(user.user_id, len(book))
    text = book[len(book)]
    keyboard_args = get_pagination_keyboard_args(len(book), book)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
        )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@user_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    text = book[int(callback.data)]
    user = db.get_user(callback.from_user.id)
    db.update_user_page(user.user_id, int(callback.data))
    keyboard_args = get_pagination_keyboard_args(user.current_page, book)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(*keyboard_args),
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@user_router.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *db.get_user(callback.from_user.id).bookmarks, book=book
        ),
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@user_router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON["cancel_text"])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@user_router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery, book: dict, db: JSONDatabase):
    user = db.get_user(callback.from_user.id)
    db.remove_bookmark(user.user_id, int(callback.data[:-3]))
    if user.bookmarks:
        await callback.message.edit_text(
            text=LEXICON["/bookmarks"],
            reply_markup=create_edit_keyboard(
                *user.bookmarks, book=book
            ),
        )
    else:
        await callback.message.edit_text(text=LEXICON["no_bookmarks"])

