from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.settings import settings
from core.models import Branch, OurSite

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='💰 Баланс бонусов',
                callback_data='bonus_balance',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🔎 Онлайн оценка',
                callback_data='online_evaluation',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🏪 Адреса и контакты',
                callback_data='branches',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🌐 Наши сайты',
                callback_data='our_sites',
            ),
            InlineKeyboardButton(
                text='📲 Наши соцсети',
                callback_data='social_media',
            ),
        ],
    ],
)

to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='В меню', callback_data='to_menu')],
    ],
)

social_media_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📱 ВК', url=settings.VK_URL),
            InlineKeyboardButton(text='📩 Телеграм', url=settings.TG_URL),
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='switch_to_menu_kb',
            ),
        ],
    ],
)

back_button_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='switch_to_menu_kb',
            ),
        ],
    ],
)

evaluation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Загрузить фото',
                callback_data='upload_photo',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='switch_to_menu_kb',
            ),
        ],
    ],
)


yes_no_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Нет',
                callback_data='no',
            ),
        ],
    ],
)


def get_branch_keyboard(branch: Branch):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Менеджер', url=branch.manager_url)],
            [
                InlineKeyboardButton(
                    text='Построить маршрут',
                    url=branch.address_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data='delete_branch_message',
                ),
            ],
        ],
    )


async def get_our_sites_keyboard():
    kb = InlineKeyboardBuilder()
    async for obj in OurSite.objects.all():
        kb.button(text=obj.text, url=obj.url)
    kb.button(text='Назад', callback_data='switch_to_menu_kb')
    return kb.adjust(1).as_markup()
