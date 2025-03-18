from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_button_kb

router = Router()


@router.callback_query(F.data == 'branches')
async def branches(query: CallbackQuery):
    await query.message.edit_text(
        'Наши филиалы',
        reply_markup=back_button_kb,
    )
