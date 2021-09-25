from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Cancel')
        ],
    ],
    resize_keyboard=True
)
