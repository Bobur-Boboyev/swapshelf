from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from config import settings
from utils import states
from handlers import start, shelf


def main() -> None:
    updater = Updater(settings.BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start.start)],
            states={
                states.RegistrationStates.SET_NAME: [
                    MessageHandler(Filters.text & ~Filters.command, start.set_name)
                ],
                states.RegistrationStates.SET_PHONE: [
                    MessageHandler(Filters.text & ~Filters.command, start.set_phone)
                ],
                states.RegistrationStates.CONFIRM: [
                    CallbackQueryHandler(start.register, pattern="^(ha)$"),
                    CallbackQueryHandler(start.start, pattern="^(yo'q)$"),
                ],
            },
            fallbacks=[CommandHandler("start", start.start)],
        )
    )

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(shelf.ask_title, pattern="^(add_book)$")
            ],
            states={
                states.AddBookStates.SET_TITLE: [
                    MessageHandler(Filters.text & ~Filters.command, shelf.set_title)
                ],
                states.AddBookStates.SET_AUTHOR: [
                    MessageHandler(Filters.text & ~Filters.command, shelf.set_author)
                ],
                states.AddBookStates.SET_GENRE: [
                    CallbackQueryHandler(shelf.set_genre, pattern="add_book:genre:")
                ],
                states.AddBookStates.SET_STATUS: [
                    CallbackQueryHandler(shelf.set_status, pattern="add_book:status:")
                ],
                states.AddBookStates.TYPE: [
                    CallbackQueryHandler(shelf.set_type, pattern="add_book:type:")
                ],
                states.AddBookStates.CONFIRM: [
                    CallbackQueryHandler(shelf.add_book, pattern="^(ha)$"),
                    CallbackQueryHandler(start.start, pattern="^(yo'q)$"),
                ],
            },
            fallbacks=[CommandHandler("start", start.start)],
        )
    )

    dispatcher.add_handler(
        CallbackQueryHandler(shelf.show_my_books, pattern="my_books")
    )

    dispatcher.add_handler(CallbackQueryHandler(shelf.share_book, pattern="share:"))

    dispatcher.add_handler(CallbackQueryHandler(shelf.get_back_to_menu, pattern="back_to_menu"))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
