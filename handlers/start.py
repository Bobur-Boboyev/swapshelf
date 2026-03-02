from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from utils import states
from keyboards.inline import get_confirm_keyboard, get_menu_keyboard
from db.users import create_user, get_user


def start(update: Update, context: CallbackContext) -> int:
    existing_user = get_user(update.effective_user.id)
    if existing_user:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Xush kelibsiz, {existing_user[2]}! Siz allaqachon ro'yxatdan o'tgansiz.",
            reply_markup=get_menu_keyboard(),
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
    query.edit_message_text("Ro'yxatdan o'tdingiz! Rahmat!")

    user_id = update.effective_user.id
    name = context.user_data["name"]
    phone = context.user_data["phone"]
    create_user(user_id, name, phone)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Xush kelibsiz, {name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
        reply_markup=get_menu_keyboard(),
    )

    return ConversationHandler.END
