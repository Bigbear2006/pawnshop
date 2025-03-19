from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot.api import SmartLombardAPI
from bot.keyboards.inline import menu_kb
from bot.keyboards.reply import request_contact_kb
from bot.loader import logger
from core.models import Client

router = Router()


@router.message(Command('start'))
async def start(msg: Message):
    client, created = await Client.objects.create_or_update_from_tg_user(
        msg.from_user,
    )
    if created:
        logger.info(f'New client {client} id={client.pk} was created')
    else:
        logger.info(f'Client {client} id={client.pk} was updated')

    if client.smart_lombard_id:
        await msg.answer(
            f'Привет, {msg.from_user.full_name}!',
            reply_markup=menu_kb
        )
        return

    await msg.answer(
        'Отправьте свой номер телефона, чтобы зарегистрироваться.',
        reply_markup=request_contact_kb,
    )


@router.message(F.contact | F.text, StateFilter(None))
async def auth(msg: Message):
    phone = f'+{msg.contact.phone_number}' if msg.contact else f'+{msg.text}'
    logger.info(phone)
    client = await SmartLombardAPI.get_client_by_phone(phone)

    if not client:
        await msg.answer('Пользователя с таким номером телефона нет.')
        return

    await Client.objects.filter(pk=msg.chat.id)\
        .aupdate(phone=client['phone'], smart_lombard_id=client['id'])

    message = await msg.answer(
        'Вы успешно авторизовались по номеру телефона.',
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer(
        f'Привет, {msg.from_user.full_name}!',
        reply_markup=menu_kb,
    )


@router.callback_query(F.data == 'to_menu')
async def switch_to_menu_kb(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer(
        'Вы перешли в главное меню',
        reply_markup=menu_kb,
    )


@router.callback_query(F.data == 'switch_to_menu_kb')
async def switch_to_menu_kb(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(
        'Вы перешли в главное меню',
        reply_markup=menu_kb,
    )
