from telegram.ext import CallbackContext
from telegram import Update

from keyboards.inline import back_to_menu_keyboard, answer_request_keyboard
from db.services import UserService, SwapRequestService, SwapService, BookService
from db.session import SessionLocal

session = SessionLocal()

user_service = UserService(session)
swap_request_service = SwapRequestService(session)
swap_service = SwapService(session)
book_service = BookService(session)


def request_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    book_id = query.data.split(":")[-1]

    user = user_service.get_user_by_tg_id(query.from_user.id)
    book = book_service.get_book_by_id(book_id)

    if user:
        request = swap_request_service.create_request(user.id, book.id)
        if request:
            context.bot.send_message(
                chat_id=book.user.telegram_id,
                text=f"{book.title} kitobi uchun so'rov keldi. tasdiqlash uchun quyidagi tugmani bosing.",
                reply_markup=answer_request_keyboard(book.id, user.id),
            )

            query.edit_message_text(
                f"{book.title} kitobi so'rov yuborildi!",
                reply_markup=back_to_menu_keyboard(),
            )
        else:
            query.edit_message_text(
                f"{book.title} kitobi uchun allaqachon so'rov yuborgansiz!",
                reply_markup=back_to_menu_keyboard(),
            )

    else:
        query.edit_message_text(
            "nimadir xato ketdi, iltimos qayta urinib ko'ring.",
            reply_markup=back_to_menu_keyboard(),
        )


def show_my_requests(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = user_service.get_user_by_tg_id(query.from_user.id)
    if not user:
        query.edit_message_text(
            "Foydalanuvchi topilmadi.", reply_markup=back_to_menu_keyboard()
        )
        return

    requests = user.requests
    if not requests:
        query.edit_message_text(
            "Sizning so'rovingiz yo'q.", reply_markup=back_to_menu_keyboard()
        )
        return

    message = "Sizning so'rovingiz:\n\n"
    for req in requests:
        book = req.book

        message += f"📖 {book.title} - Holati: {req.status.value}\n"

    query.edit_message_text(message, reply_markup=back_to_menu_keyboard())
