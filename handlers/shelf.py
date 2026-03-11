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
    back_to_menu_keyboard,
    get_books_by_genre_keyboard,
    request_book_in_channel_keyboard,
)
from db.services import BookService, GenreService, UserService
from db.session import SessionLocal
from config import settings

session = SessionLocal()

book_service = BookService(session)
genre_service = GenreService(session)
user_service = UserService(session)


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
    genre_id = context.user_data["genre"]
    status = context.user_data["status"]
    type_ = context.user_data["type"]

    genre = genre_service.get_genre_by_id(genre_id)

    query.edit_message_text(
        f"Kitob nomi: {title}\n"
        f"Muallif: {author}\n"
        f"Janr: {genre.name}\n"
        f"Holat: {status}\n"
        f"Tur: {type_}\n"
        "Tasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard(),
    )
    return states.AddBookStates.CONFIRM


def add_book(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    title = context.user_data["title"]
    author = context.user_data["author"]
    genre_id = context.user_data["genre"]
    status = context.user_data["status"]
    type_ = context.user_data["type"]
    added_by = user_service.get_user_by_tg_id(query.from_user.id)

    book = book_service.add_book(
        title=title,
        author=author,
        genre_id=genre_id,
        status=status,
        type_=type_,
        added_by=added_by.id,
    )
    query.edit_message_text(f"{book.title} Kitob qo'shildi! Rahmat!")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📖 {book.title}\n✍️ {book.author}\n📚 {book.genre.name}\n🔖 {book.status.value}\n🔄 {book.type_.value}\n\n",
        reply_markup=get_book_action_keyboard(book.id),
    )

    return ConversationHandler.END


def show_my_books(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = user_service.get_user_by_tg_id(query.from_user.id)
    books = user.books
    if not books:
        update.callback_query.edit_message_text(
            "Sizning javoningizda kitob yo'q.", reply_markup=back_to_menu_keyboard()
        )
        return

    message = "Sizning javoningizdagi kitoblar:\n\n"
    for book in books:
        message += f"📖 {book.title}\n✍️ {book.author}\n📚 {book.genre.name}\n🔖 {book.status.value}\n🔄 {book.type_.value}\n\n"
    update.callback_query.edit_message_text(
        message, reply_markup=back_to_menu_keyboard()
    )


def share_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    book_id = query.data.split(":")[-1]
    book = book_service.get_book_by_id(book_id)

    if not book:
        query.edit_message_text("Kitob topilmadi.")
        return

    context.bot.send_message(
        chat_id=settings.CHANNEL_ID,
        text=f"📖 {book.title}\n✍️ {book.author}\n📚 {book.genre.name}\n🔖 {book.status.value}\n🔄 {book.type_.value}\n",
        reply_markup=request_book_in_channel_keyboard(book.id),
    )
    query.edit_message_text(
        f"{book.title} kitobi almashish uchun kanalga yuborildi!",
        reply_markup=back_to_menu_keyboard(),
    )


def get_back_to_menu(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        "Asosiy menyu:", reply_markup=get_menu_keyboard()
    )


def browse_books(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Kitob janrini kiriting:",
        reply_markup=get_genre_keyboard(),
    )


def show_book_details_by_genre(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    genre_id = query.data.split(":")[-1]

    genre = genre_service.get_genre_by_id(genre_id)
    books = genre.books

    if not books:
        query.edit_message_text(
            f"{genre.name} janrida kitob topilmadi.",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    for book in books:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📖 {book.title}\n✍️ {book.author}\n📚 {book.genre.name}\n🔖 {book.status.value}\n🔄 {book.type_.value}\n",
            reply_markup=get_books_by_genre_keyboard(book.id),
        )
