from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_button_kb

router = Router()


@router.callback_query(F.data == 'online_evaluation')
async def online_evaluation(query: CallbackQuery):
    await query.message.edit_text(
        'Онлайн оценка',
        reply_markup=back_button_kb,
    )
