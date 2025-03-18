from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.settings import settings

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Баланс бонусов', callback_data='bonus_balance')],
        [InlineKeyboardButton(text='Филиалы', callback_data='branches')],
        [InlineKeyboardButton(text='Онлайн оценка', callback_data='online_evaluation')],
        [
            InlineKeyboardButton(text='Наши соцсети', callback_data='social_media'),
            InlineKeyboardButton(text='Наш сайт', url=settings.SITE_URL),
        ],
    ]
)

social_media_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ВК', url=settings.VK_URL),
            InlineKeyboardButton(text='Телеграм', url=settings.TG_URL),
        ],
        [InlineKeyboardButton(text='Назад', callback_data='switch_to_menu_kb')]
    ]
)

back_button_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='switch_to_menu_kb')]
    ]
)