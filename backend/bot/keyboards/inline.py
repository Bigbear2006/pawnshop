from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.db.models import Model

from bot.settings import settings
from core.models import Branch

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
                text='🏪 Адреса и контакты', callback_data='branches',
            ),
        ],
        [
            InlineKeyboardButton(
                text='🚗 Автозаймы',
                url=settings.AUTOLOAN_SITE_URL,
            ),
        ],
        [
            InlineKeyboardButton(
                text='📲 Наши соцсети',
                callback_data='social_media',
            ),
            InlineKeyboardButton(text='🌐 Наш сайт', url=settings.SITE_URL),
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


def one_button_keyboard(
    *,
    back_button_data: str = None,
    **kwargs,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(**kwargs)
    if back_button_data:
        kb.button(text='Назад', callback_data=back_button_data)

    kb.adjust(1)
    return kb.as_markup()


async def keyboard_from_queryset(
    model: type[Model],
    *,
    prefix: str,
    back_button_data: str = None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    async for obj in model.objects.all():
        kb.button(text=str(obj), callback_data=f'{prefix}_{obj.pk}')

    if back_button_data:
        kb.button(text='Назад', callback_data=back_button_data)

    kb.adjust(1)
    return kb.as_markup()


def get_branch_keyboard(branch: Branch):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Менеджер', url=branch.manager_url)],
            [InlineKeyboardButton(text='Построить маршрут', url=branch.address_url)],
            [InlineKeyboardButton(text='Назад', callback_data='delete_branch_message')],
        ],
    )
