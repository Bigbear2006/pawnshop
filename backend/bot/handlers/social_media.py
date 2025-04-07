from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline import social_media_kb

router = Router()


@router.callback_query(F.data == 'social_media')
async def social_media(query: CallbackQuery):
    await query.message.edit_caption(
        caption='Наши соцсети',
        reply_markup=social_media_kb,
    )
