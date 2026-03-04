from telegram.ext import CallbackContext
from telegram import Update

from keyboards.inline import back_to_menu_keyboard, answer_request_keyboard
from db.users import get_user_by_id, get_user_by_tg_id
from db.requests import (
    save_book_request,
    get_my_requests,
    update_request_status,
    find_request_id,
)
from db.swaps import create_swap
from db.books import get_book


def request_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    book_id = query.data.split(":")[-1]

    user = get_user_by_tg_id(query.from_user.id)
    book = get_book(book_id)

    print(f"User {user} is requesting book {book}")

    if user:
        save_book_request(user[0], book_id, "Pending")
        context.bot.send_message(
            chat_id=get_user_by_id(book[6])[1],
            text=f"{book[1]} kitobi uchun so'rov keldi. tasdiqlash uchun quyidagi tugmani bosing.",
            reply_markup=answer_request_keyboard(book_id, user[0]),
        )

        query.edit_message_text(
            "Kitob so'rov yuborildi!", reply_markup=back_to_menu_keyboard()
        )
    else:
        query.edit_message_text(
            "nimadir xato ketdi, iltimos qayta urinib ko'ring.",
            reply_markup=back_to_menu_keyboard(),
        )


def show_my_requests(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = get_user_by_tg_id(query.from_user.id)
    if not user:
        query.edit_message_text(
            "Foydalanuvchi topilmadi.", reply_markup=back_to_menu_keyboard()
        )
        return

    requests = get_my_requests(user[0])
    if not requests:
        query.edit_message_text(
            "Sizning so'rovingiz yo'q.", reply_markup=back_to_menu_keyboard()
        )
        return

    message = "Sizning so'rovingiz:\n\n"
    for req in requests:
        book = get_book(req[0])
        message += f"📖 {book[1]} - Holati: {req[2]}\n"

    query.edit_message_text(message, reply_markup=back_to_menu_keyboard())
