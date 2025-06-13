from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    Message,
    ReplyKeyboardRemove,
)

from bot.api import SmartLombardAPI
from bot.keyboards.inline import menu_kb, yes_no_kb
from bot.keyboards.reply import request_contact_kb
from bot.loader import logger
from bot.schemas import RegistrationData
from bot.states import RegistrationState
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
        await msg.answer_photo(
            FSInputFile('bot/assets/start.png'),
            f'Привет, {msg.from_user.full_name}!',
            reply_markup=menu_kb,
        )
        return

    await msg.answer(
        'Отправьте свой номер телефона в международном формате, '
        'чтобы зарегистрироваться.\nНомер должен начинаться с +',
        reply_markup=request_contact_kb,
    )


@router.message(F.contact | F.text, StateFilter(None))
async def login(msg: Message, state: FSMContext):
    phone = msg.contact.phone_number if msg.contact else msg.text
    phone = phone if phone.startswith('+') else f'+{phone}'
    logger.info(phone)

    client = await SmartLombardAPI.get_client_by_phone(phone)
    if not client:
        await state.update_data(phone=phone)
        await state.set_state(RegistrationState.confirmation)
        await msg.answer(
            'Пользователя с таким номером телефона нет.\n'
            'Хотите зарегистрировать по этому номеру телефона?',
            reply_markup=yes_no_kb,
        )
        return

    await Client.objects.filter(pk=msg.chat.id).aupdate(
        phone=client['phone'],
        smart_lombard_id=client['id'],
    )

    message = await msg.answer(
        'Вы успешно авторизовались по номеру телефона.',
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer_photo(
        FSInputFile('bot/assets/start.png'),
        f'Привет, {msg.from_user.full_name}!',
        reply_markup=menu_kb,
    )


@router.callback_query(
    F.data == 'yes',
    StateFilter(RegistrationState.confirmation),
)
async def confirmation_yes(query: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.name)
    await query.message.edit_text(
        'Введите свое фамилию и имя через пробел.\nПример: Иванов Иван',
        reply_markup=None,
    )


@router.callback_query(
    F.data == 'no',
    StateFilter(RegistrationState.confirmation),
)
async def confirmation_no(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(
        'Вы отменили регистрацию по номеру телефона.',
        reply_markup=None,
    )


@router.message(F.text, StateFilter(RegistrationState.name))
async def set_name(msg: Message, state: FSMContext):
    last_name, name = msg.text.split()
    await state.update_data(last_name=last_name, name=name)

    await state.set_state(RegistrationState.birth_date)
    await msg.answer(
        'Введите свою дату рождения.\nПример: 18.06.2002',
    )


@router.message(F.text, StateFilter(RegistrationState.birth_date))
async def set_birth_date(msg: Message, state: FSMContext):
    await state.update_data(birth_date=msg.text)
    data = await state.get_data()
    logger.info(data)
    rsp_data = await SmartLombardAPI.register(RegistrationData(**data))

    if rsp_data['status']:
        await Client.objects.filter(pk=msg.chat.id).aupdate(
            phone=data['phone'],
            smart_lombard_id=rsp_data['result']['natural_person_id'],
        )
        await msg.answer(
            'Вы успешно зарегистрировались!\n',
            reply_markup=ReplyKeyboardRemove(),
        )
        await msg.answer_photo(
            FSInputFile('bot/assets/start.png'),
            'Вы перешли в главное меню',
            reply_markup=menu_kb,
        )
    else:
        await msg.answer('К сожалению, во время регистрации произошла ошибка.')

    await state.clear()


@router.callback_query(F.data == 'to_menu')
async def to_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer_photo(
        FSInputFile('bot/assets/start.png'),
        'Вы перешли в главное меню',
        reply_markup=menu_kb,
    )


@router.callback_query(F.data == 'switch_to_menu_kb')
async def switch_to_menu_kb(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_caption(
        caption='Вы перешли в главное меню',
        reply_markup=menu_kb,
    )
