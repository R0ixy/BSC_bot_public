from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Get Balance")
        ],
        [
            KeyboardButton(text="Wallet"),
            KeyboardButton(text="Settings"),
        ],
        [
            KeyboardButton(text="Donate"),
        ],
    ],
    resize_keyboard=True
)
