from telegram.ext import CallbackContext
from telegram import Update

from db.users import get_user_by_tg_id
from db.review import get_reviews_for_user
from keyboards.inline import back_to_menu_keyboard


def view_profile(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_info = get_user_by_tg_id(query.from_user.id)
    reviews = get_reviews_for_user(user_info[0])
    average_rating = sum([r[0] for r in reviews]) / len(reviews) if reviews else 0
    name = user_info[2]
    phone = user_info[3]
    query.edit_message_text(
        f"Ism: {name}\nTel: {phone}\nRating: {average_rating:.2f}",
        reply_markup=back_to_menu_keyboard(),
    )
