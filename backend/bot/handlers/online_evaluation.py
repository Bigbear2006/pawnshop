from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import evaluation_kb, to_menu_kb
from bot.settings import settings
from bot.states import EvaluationState
from core.models import Client, OnlineEvaluationGuide

router = Router()


@router.callback_query(F.data == 'online_evaluation')
async def online_evaluation(query: CallbackQuery):
    guide = await OnlineEvaluationGuide.objects.afirst()
    await query.message.edit_caption(
        caption=guide.text,
        reply_markup=evaluation_kb,
    )


@router.callback_query(F.data == 'upload_photo')
async def upload_photo(query: CallbackQuery, state: FSMContext):
    await state.set_state(EvaluationState.photo)
    await query.message.answer('Загрузите фото')


@router.message(F.photo, StateFilter(EvaluationState.photo))
async def set_photo(msg: Message, state: FSMContext):
    await state.update_data(photo=msg.photo[0].file_id)
    await state.set_state(EvaluationState.amount)
    await msg.answer('Укажите желаемую сумму')


@router.message(F.text, StateFilter(EvaluationState.amount))
async def set_amount(msg: Message, state: FSMContext):
    try:
        amount = int(msg.text)
    except ValueError:
        await msg.answer('Введите корректную сумму')
        return

    if amount <= 0:
        await msg.answer('Введите корректную сумму')
        return

    client = await Client.objects.aget(pk=msg.chat.id)
    caption = (
        f'Онлайн оценка\n\nЖелаемая сумма: {amount}\nТелефон: {client.phone}\n'
    )
    if msg.chat.username:
        caption += f'Юзернейм @{msg.chat.username}'

    await msg.bot.send_photo(
        settings.FORWARD_CHAT_ID,
        await state.get_value('photo'),
        caption=caption,
    )

    await state.clear()
    await msg.answer(
        'Готово, в ближайшее время с вами свяжется наш менеджер',
        reply_markup=to_menu_kb,
    )
