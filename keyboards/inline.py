from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from db.books import get_genres
from config import Settings


def get_confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Ha", callback_data="ha"),
            InlineKeyboardButton("Yo'q", callback_data="yo'q"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Mening Javonim", callback_data="my_books")],
        [InlineKeyboardButton("➕ Kitob Qo'shish", callback_data="add_book")],
        [InlineKeyboardButton("🔍 Kitob Qidirish", callback_data="browse_books")],
        [InlineKeyboardButton("📬 Mening So'rovlaram", callback_data="my_requests")],
        [InlineKeyboardButton("🔄 Mening Almashtirishlarim", callback_data="my_swaps")],
        [InlineKeyboardButton("⭐ Mening Sahifam", callback_data="my_profile")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_genre_keyboard():
    genres = get_genres()
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"add_book:genre:{genre_id}")]
        for genre_id, name in genres
    ]
    return InlineKeyboardMarkup(keyboard)


def get_status_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🆕 Yangi, ishlatilmagan", callback_data="add_book:status:New"
            )
        ],
        [
            InlineKeyboardButton(
                "👍 Yaxshi holatda", callback_data="add_book:status:Good"
            )
        ],
        [
            InlineKeyboardButton(
                "👌 O'rtacha holatda", callback_data="add_book:status:Fair"
            )
        ],
        [
            InlineKeyboardButton(
                "📄 Ko'p ishlatilgan", callback_data="add_book:status:Worn"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_type_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Vaqtincha (30 kun muddatli)", callback_data="add_book:type:Borrow"
            )
        ],
        [
            InlineKeyboardButton(
                "🎁 Doimiy berib yuborish", callback_data="add_book:type:Permanent"
            )
        ],
        [
            InlineKeyboardButton(
                "🔀 Ikkalasi ham mumkin", callback_data="add_book:type:Both"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_book_action_keyboard(book_id):
    keyboard = [
        [InlineKeyboardButton("🎁 Kitobni Ulashish", callback_data=f"share:{book_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_book_request_keyboard(book_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Kitobni olish uchun bosing", callback_data=f"request:{book_id}"
            ),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_books_by_genre_keyboard(book_id):
    keyboard = [
        [InlineKeyboardButton("Bosh sahifaga qaytish", callback_data="back_to_menu")],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_genre_selection"),
        ],
        [
            InlineKeyboardButton(
                "✅ Kitobni olish uchun bosing", callback_data=f"request:{book_id}"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def answer_request_keyboard(book_id, requester_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ So'rovni qabul qilish",
                callback_data=f"answer_request:accept:{book_id}:{requester_id}",
            ),
            InlineKeyboardButton(
                "❌ So'rovni rad etish",
                callback_data=f"answer_request:reject:{book_id}:{requester_id}",
            ),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def request_book_in_channel_keyboard(book_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ So'rov yuborish",
                url=f"https://t.me/{Settings.BOT_USERNAME}?start=request_{book_id}",
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
