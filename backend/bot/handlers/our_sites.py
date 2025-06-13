from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_our_sites_keyboard

router = Router()


@router.callback_query(F.data == 'our_sites')
async def our_sites(query: CallbackQuery):
    await query.message.edit_caption(
        caption='Наши сайты',
        reply_markup=await get_our_sites_keyboard(),
    )
