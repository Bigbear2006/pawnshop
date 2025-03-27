from urllib.parse import unquote

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, BufferedInputFile, InputMediaPhoto

from bot.keyboards.inline import (
    get_branch_keyboard,
    keyboard_from_queryset,
)
from core.models import Branch

router = Router()


@router.callback_query(F.data == 'branches')
async def branches(query: CallbackQuery, state: FSMContext):
    await state.update_data(branch_message_id=None)

    await query.message.edit_text(
        'Список наших филиалов',
        reply_markup=await keyboard_from_queryset(
            Branch,
            prefix='branch',
            back_button_data='switch_to_menu_kb',
        ),
    )


@router.callback_query(F.data.startswith('branch'))
async def display_branch(query: CallbackQuery, state: FSMContext):
    branch_message_id = await state.get_value('branch_message_id')
    branch = await Branch.objects.aget(pk=query.data.split('_')[-1])

    media = BufferedInputFile.from_file(unquote(branch.photo.url.lstrip('/')))
    caption = f'📍 {branch.title} ({branch.work_schedule})\n\n' \
              f'📲 {branch.phone}'

    if branch_message_id:
        try:
            await query.bot.edit_message_media(
                InputMediaPhoto(media=media, caption=caption),
                query.message.business_connection_id,
                query.message.chat.id,
                branch_message_id,
                reply_markup=get_branch_keyboard(branch),
            )
            return
        except TelegramBadRequest:
            pass
    else:
        branch_message = await query.message.answer_photo(
            media,
            caption,
            reply_markup=get_branch_keyboard(branch),
        )
        await state.update_data(
            branch_message_id=branch_message.message_id,
        )


@router.callback_query(F.data == 'delete_branch_message')
async def delete_branch_message(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.update_data(branch_message_id=None)
