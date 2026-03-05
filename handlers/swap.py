from telegram.ext import CallbackContext
from telegram import Update

from keyboards.inline import (
    back_to_menu_keyboard,
    return_book_keyboard,
    give_feedback_keyboard,
)
from db.users import get_user_by_id, get_user_by_tg_id
from db.requests import find_request_id, update_request_status
from db.swaps import create_swap, get_my_swaps, update_swap_status, get_swap_by_id
from db.books import get_book
from db.review import create_review


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


def show_my_swaps(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user_info = get_user_by_tg_id(query.from_user.id)
    user_id = user_info[0]
    swaps = get_my_swaps(user_id)

    if not swaps:
        query.edit_message_text(
            "Hozircha hech qanday almashtirishlaringiz yo'q.",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    for swap in swaps:
        swap_id, status, book_title, responder_username = swap

        query.message.reply_text(
            f"Kitob: {book_title}\nStatus: {status}\nKimdan: {responder_username}",
            reply_markup=return_book_keyboard(swap_id),
        )

    query.message.reply_text(
        "Bu sizning barcha almashtirishlaringiz.", reply_markup=back_to_menu_keyboard()
    )


def return_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    swap_id = query.data.split(":")[1]

    update_swap_status(swap_id, "Completed")

    query.message.reply_text(
        "kitob uchun feedback bering", reply_markup=give_feedback_keyboard(swap_id)
    )

    query.edit_message_text(
        "Kitobni qaytarish jarayoni boshlandi. Iltimos, kitobni qabul qiluvchiga qaytaring va ular bilan bog'laning.",
        reply_markup=back_to_menu_keyboard(),
    )


def create_feedback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    _, swap_id, feedback = query.data.split(":")

    reviewer = get_user_by_tg_id(query.from_user.id)
    reviewer_id = reviewer[0]

    swap_info = get_swap_by_id(swap_id)
    reviewee_id = swap_info[3]

    create_review(reviewer_id=reviewer_id, reviewee_id=reviewee_id, rating=feedback)

    query.edit_message_text(
        "Rahmat! Sizning fikringiz biz uchun muhim.",
        reply_markup=back_to_menu_keyboard(),
    )
