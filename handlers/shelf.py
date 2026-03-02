from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils import states
from keyboards.inline import (
    get_confirm_keyboard,
    get_genre_keyboard,
    get_menu_keyboard,
    get_status_keyboard,
    get_type_keyboard,
    get_book_action_keyboard,
    get_book_request_keyboard,
    back_to_menu_keyboard
)
from db.books import create_book, get_my_books, get_book
from config import settings


def ask_title(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    update.callback_query.edit_message_text("Kitob nomini kiriting:")
    return states.AddBookStates.SET_TITLE


def set_title(update: Update, context: CallbackContext) -> int:
    context.user_data["title"] = update.message.text
    update.message.reply_text("Kitob muallifini kiriting:")
    return states.AddBookStates.SET_AUTHOR


def set_author(update: Update, context: CallbackContext) -> int:
    context.user_data["author"] = update.message.text
    update.message.reply_text(
        "Kitob janrini tanlang:", reply_markup=get_genre_keyboard()
    )
    return states.AddBookStates.SET_GENRE


def set_genre(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    genre = query.data.split(":")[-1]
    context.user_data["genre"] = genre
    query.edit_message_text(
        "Kitob holatini tanlang:", reply_markup=get_status_keyboard()
    )
    return states.AddBookStates.SET_STATUS


def set_status(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    status = query.data.split(":")[-1]
    context.user_data["status"] = status
    query.edit_message_text("Kitob turini tanlang:", reply_markup=get_type_keyboard())
    return states.AddBookStates.TYPE


def set_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    book_type = query.data.split(":")[-1]
    context.user_data["type"] = book_type
    title = context.user_data["title"]
    author = context.user_data["author"]
    genre = context.user_data["genre"]
    status = context.user_data["status"]
    type_ = context.user_data["type"]
    query.edit_message_text(
        f"Kitob nomi: {title}\n"
        f"Muallif: {author}\n"
        f"Janr: {genre}\n"
        f"Holat: {status}\n"
        f"Tur: {type_}\n"
        "Tasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard(),
    )
    return states.AddBookStates.CONFIRM


def add_book(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text("Kitob qo'shildi! Rahmat!")

    book_id = create_book(
        telegram_id=update.effective_user.id,
        title=context.user_data["title"],
        author=context.user_data["author"],
        genre_id=context.user_data["genre"],
        status=context.user_data["status"],
        type_=context.user_data["type"],
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📖 {context.user_data['title']}\n✍️ {context.user_data['author']}\n📚 {context.user_data['genre']}\n🔖 {context.user_data['status']}\n🔄 {context.user_data['type']}\n\n",
        reply_markup=get_book_action_keyboard(book_id),
    )

    return ConversationHandler.END


def show_my_books(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()

    books = get_my_books(update.effective_user.id)
    if not books:
        update.callback_query.edit_message_text("Sizning javoningizda kitob yo'q.", reply_markup=back_to_menu_keyboard())
        return
    message = "Sizning javoningizdagi kitoblar:\n\n"
    for pk, title, author, genre, status, type_ in books:
        message += f"📖 {title}\n✍️ {author}\n📚 {genre}\n🔖 {status}\n🔄 {type_}\n\n"
    update.callback_query.edit_message_text(message, reply_markup=back_to_menu_keyboard())


def share_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    book_id = query.data.split(":")[-1]
    book = get_book(book_id)
    if not book:
        query.edit_message_text("Kitob topilmadi.")
        return
    title, author, genre, status, type_ = book[1], book[2], book[3], book[4], book[5]
    context.bot.send_message(
        chat_id=settings.CHANNEL_ID,
        text=f"📖 {title}\n✍️ {author}\n📚 {genre}\n🔖 {status}\n🔄 {type_}\n",
        reply_markup=get_book_request_keyboard(book_id),
    )
    query.edit_message_text("Kitob almashish uchun kanalga yuborildi!", reply_markup=back_to_menu_keyboard())

def get_back_to_menu(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text("Asosiy menyu:", reply_markup=get_menu_keyboard())
