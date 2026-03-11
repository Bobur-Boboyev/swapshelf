from telegram.ext import CallbackContext
from telegram import Update

from db.services import UserService
from db.session import SessionLocal
from keyboards.inline import back_to_menu_keyboard

session = SessionLocal()

user_service = UserService(session)


def view_profile(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user = user_service.get_user_by_tg_id(query.from_user.id)
    rating = user.rating
    name = user.full_name
    phone = user.phone_number
    query.edit_message_text(
        f"Ism: {name}\nTel: {phone}\nRating: {rating:.2f}",
        reply_markup=back_to_menu_keyboard(),
    )
