from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_button_kb

router = Router()


@router.callback_query(F.data == 'bonus_balance')
async def bonus_balance(query: CallbackQuery):
    await query.message.edit_text(
        'Ваш бонусный баланс',
        reply_markup=back_button_kb,
    )
