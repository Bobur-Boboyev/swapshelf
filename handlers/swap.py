from telegram.ext import CallbackContext
from telegram import Update

from keyboards.inline import back_to_menu_keyboard
from db.users import get_user_by_id, get_user_by_tg_id
from db.requests import find_request_id, update_request_status
from db.swaps import create_swap
from db.books import get_book


def accept_request(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split(":")
    book_id, requester_id = data[2], data[3]

    requester_info = get_user_by_id(user_id=requester_id)
    requester_tg_id = requester_info[1]
    requester_name = requester_info[2]
    requester_phone = requester_info[3]

    responder_info = get_user_by_tg_id(query.from_user.id)
    responder_id = responder_info[0]
    responder_name = responder_info[2]
    responder_phone = responder_info[3]

    request_id = find_request_id(requester_id, book_id)
    update_request_status(request_id, "Accepted")
    create_swap(
        swap_request_id=request_id,
        requester_id=requester_id,
        responder_id=responder_id,
        book_id=book_id,
        status="Active",
    )

    context.bot.send_message(
        chat_id=requester_tg_id,
        text=f"Sizning {get_book(book_id)[1]} kitobiga bo'lgan so'rovingiz qabul qilindi!\n\nKitob egasi: {responder_name}\ntel: {responder_phone}",
        reply_markup=back_to_menu_keyboard(),
    )

    query.edit_message_text(
        text=f"Qabul qilib oluvchi: {requester_name}\ntel: {requester_phone}",
        reply_markup=back_to_menu_keyboard(),
    )


def reject_request(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split(":")
    book_id, requester_id = data[2], data[3]

    requester_info = get_user_by_id(user_id=requester_id)
    requester_tg_id = requester_info[1]

    responder_info = get_user_by_tg_id(query.from_user.id)
    responder_id = responder_info[0]

    request_id = find_request_id(requester_id, book_id)
    print(request_id)
    update_request_status(request_id, "Rejected")
    create_swap(
        swap_request_id=request_id,
        requester_id=requester_id,
        responder_id=responder_id,
        book_id=book_id,
        status="Cancelled",
    )

    context.bot.send_message(
        chat_id=requester_tg_id,
        text=f"Sizning {get_book(book_id)[1]} kitobiga bo'lgan so'rovingiz rad etildi!",
        reply_markup=back_to_menu_keyboard(),
    )

    query.edit_message_text(
        "So'rovni rad etdingiz!", reply_markup=back_to_menu_keyboard()
    )
