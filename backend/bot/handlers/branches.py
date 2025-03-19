from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_button_kb, keyboard_from_queryset, get_branch_keyboard
from core.models import Branch

router = Router()


@router.callback_query(F.data == 'branches')
async def branches(query: CallbackQuery):
    await query.message.edit_text(
        'Список наших филиалов',
        reply_markup=await keyboard_from_queryset(
            Branch,
            prefix='branch',
            back_button_data='switch_to_menu_kb',
        ),
    )


@router.callback_query(F.data.startswith('branch'))
async def branch_message(query: CallbackQuery):
    branch = await Branch.objects.aget(pk=query.data.split('_')[-1])
    return await query.message.edit_text(
        f'Филиал {branch.title}\n\nГрафик работы: {branch.work_schedule}',
        reply_markup=get_branch_keyboard(branch),
    )
