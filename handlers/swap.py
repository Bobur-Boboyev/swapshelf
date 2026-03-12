from telegram.ext import CallbackContext
from telegram import Update

from keyboards.inline import (
    back_to_menu_keyboard,
    return_book_keyboard,
    give_feedback_keyboard,
)
from db.services import (
    UserService,
    SwapRequestService,
    SwapService,
    BookService,
    ReviewService,
)
from db.session import SessionLocal

session = SessionLocal()

user_service = UserService(session)
swap_request_service = SwapRequestService(session)
swap_service = SwapService(session)
book_service = BookService(session)
review_service = ReviewService(session)


def accept_request(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split(":")
    book_id, requester_id = data[2], data[3]

    book = book_service.get_book_by_id(book_id=book_id)

    requester_info = user_service.get_user_by_id(user_id=requester_id)

    responder_info = user_service.get_user_by_tg_id(query.from_user.id)

    request = swap_request_service.get_request_by_requester_id_and_book_id(
        requester_info.id, book_id
    )
    if not request:
        query.edit_message_text(
            "So'rov topilmadi yoki allaqachon ko'rib chiqilgan.",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    swap_request_service.update_request_status(request.id, "accepted")

    swap = swap_service.create_swap(
        swap_request_id=request.id,
        requester_id=requester_info.id,
        responder_id=responder_info.id,
        book_id=book.id,
        status="active",
    )

    context.bot.send_message(
        chat_id=requester_info.telegram_id,
        text=f"Sizning {book.title} kitobiga bo'lgan so'rovingiz qabul qilindi!\n\nKitob egasi: {responder_info.full_name}\ntel: {responder_info.phone_number}",
        reply_markup=back_to_menu_keyboard(),
    )

    query.edit_message_text(
        text=f"{book.title} kitobi qabul qilib oluvchisi: {requester_info.full_name}\ntel: {requester_info.phone_number}",
        reply_markup=back_to_menu_keyboard(),
    )


def reject_request(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split(":")
    book_id, requester_id = data[2], data[3]

    book = book_service.get_book_by_id(book_id=book_id)

    requester_info = user_service.get_user_by_id(user_id=requester_id)

    responder_info = user_service.get_user_by_tg_id(query.from_user.id)

    request = swap_request_service.get_request_by_requester_id_and_book_id(
        requester_info.id, book_id
    )
    if not request:
        query.edit_message_text(
            "So'rov topilmadi yoki allaqachon ko'rib chiqilgan.",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    swap_request_service.update_request_status(request.id, "rejected")

    swap = swap_service.create_swap(
        swap_request_id=request.id,
        requester_id=requester_info.id,
        responder_id=responder_info.id,
        book_id=book.id,
        status="canceled",
    )

    context.bot.send_message(
        chat_id=requester_info.telegram_id,
        text=f"Sizning {book.title} kitobiga bo'lgan so'rovingiz rad etildi!",
        reply_markup=back_to_menu_keyboard(),
    )

    query.edit_message_text(
        "So'rovni rad etdingiz!", reply_markup=back_to_menu_keyboard()
    )


def show_my_swaps(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = user_service.get_user_by_tg_id(query.from_user.id)
    swaps = user.my_taken_swaps

    if not swaps:
        query.edit_message_text(
            "Hozircha hech qanday almashtirishlaringiz yo'q.",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    for swap in swaps:
        if swap.status.value == "active":
            query.message.reply_text(
                f"Kitob: {swap.book.title}\nStatus: {swap.status.value}\nKimdan: {swap.responder.full_name}",
                reply_markup=return_book_keyboard(swap.id),
            )

    query.message.reply_text(
        "Bu sizning barcha almashtirishlaringiz.", reply_markup=back_to_menu_keyboard()
    )


def return_book(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    swap_id = query.data.split(":")[1]

    swap = swap_service.update_swap_status(swap_id, "completed")

    query.message.reply_text(
        f"{swap.book.title} kitobi uchun feedback bering",
        reply_markup=give_feedback_keyboard(swap.id),
    )

    query.edit_message_text(
        "Kitobni qaytarish jarayoni boshlandi. Iltimos, kitobni qabul qiluvchiga qaytaring va ular bilan bog'laning.",
        reply_markup=back_to_menu_keyboard(),
    )


def create_feedback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    _, swap_id, feedback = query.data.split(":")

    reviewer = user_service.get_user_by_tg_id(query.from_user.id)

    swap_info = swap_service.get_swap_by_id(swap_id)

    review = review_service.create_review(
        reviewer_id=swap_info.requester_id,
        reviewee_id=swap_info.responder_id,
        rating=int(feedback),
    )

    query.edit_message_text(
        "Rahmat! Sizning fikringiz biz uchun muhim.",
        reply_markup=back_to_menu_keyboard(),
    )
