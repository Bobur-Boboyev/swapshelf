from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils import states
from keyboards.inline import (
    get_confirm_keyboard,
    get_menu_keyboard,
    get_book_request_keyboard,
)
from db.services import UserService, BookService
from db.session import SessionLocal

session = SessionLocal()

user_service = UserService(session)
book_service = BookService(session)


def start(update: Update, context: CallbackContext) -> int:
    args = context.args

    if args:
        context.user_data["payload"] = args[0]
    print(f"Start command received with args: {args}")

    existing_user = user_service.get_user_by_tg_id(update.effective_user.id)

    if existing_user and not args:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Xush kelibsiz, {existing_user.full_name}! Siz allaqachon ro'yxatdan o'tgansiz.",
            reply_markup=get_menu_keyboard(),
        )
        return ConversationHandler.END

    payload = context.user_data.get("payload")
    if existing_user and payload and payload.startswith("request_"):
        book_id = payload.split("_")[1]
        book = book_service.get_book_by_id(book_id=book_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Kitobni olish: {book.title}",
            reply_markup=get_book_request_keyboard(book.id),
        )
        return ConversationHandler.END

    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Assalomu alaykum! Ismingizni kiriting:"
    )

    return states.RegistrationStates.SET_NAME


def set_name(update: Update, context: CallbackContext) -> int:
    context.user_data["name"] = update.message.text
    update.message.reply_text("Telefon raqamingizni kiriting:")

    return states.RegistrationStates.SET_PHONE


def set_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["phone"] = update.message.text
    name = context.user_data["name"]
    phone = context.user_data["phone"]
    update.message.reply_text(
        f"Ismingiz: {name}\nTelefon raqamingiz: {phone}\nTasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard(),
    )

    return states.RegistrationStates.CONFIRM


def register(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user_id = update.effective_user.id
    name = context.user_data["name"]
    phone = context.user_data["phone"]
    user = user_service.register(
        full_name=name, telegram_id=user_id, phone_number=phone
    )
    query.edit_message_text("Ro'yxatdan o'tdingiz! Rahmat!")

    payload = context.user_data.get("payload")
    if not payload:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Xush kelibsiz, {user.full_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
            reply_markup=get_menu_keyboard(),
        )
        return ConversationHandler.END

    payload = context.user_data.get("payload")
    if payload and payload.startswith("request_"):
        book_id = payload.split("_")[1]
        book = book_service.get_book_by_id(book_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Kitobni olish: {book.title}",
            reply_markup=get_book_request_keyboard(book.id),
        )

    return ConversationHandler.END
