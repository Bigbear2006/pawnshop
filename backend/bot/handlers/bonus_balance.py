from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.api import SmartLombardAPI
from bot.keyboards.utils import (
    keyboard_from_queryset,
    one_button_keyboard,
)
from core.models import Client, SpendOption

router = Router()


@router.callback_query(F.data == 'bonus_balance')
async def bonus_balance(query: CallbackQuery):
    client = await Client.objects.aget(pk=query.message.chat.id)
    client = await SmartLombardAPI.get_client(client.smart_lombard_id)

    await query.message.edit_caption(
        caption=f'Ваш бонусный баланс: {client.get("bonuses") or 0} '
        f'(1 бонус = 1 рубль)\n'
        f'Вот на что их можно потратить',
        reply_markup=await keyboard_from_queryset(
            SpendOption,
            prefix='spend_option',
            back_button_data='switch_to_menu_kb',
        ),
    )


@router.callback_query(F.data.startswith('spend_option'))
async def spend_option_message(query: CallbackQuery):
    spend_option = await SpendOption.objects.aget(pk=query.data.split('_')[-1])
    await query.message.edit_caption(
        caption=spend_option.text,
        reply_markup=one_button_keyboard(
            text='Назад',
            callback_data='bonus_balance',
        ),
    )
