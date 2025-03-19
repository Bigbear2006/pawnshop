from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

request_contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поделиться контактом', request_contact=True)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
