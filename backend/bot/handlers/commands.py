import re

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

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
        await msg.answer(
            f'Привет, {msg.from_user.full_name}!',
            reply_markup=menu_kb,
        )
        return

    await msg.answer(
        'Отправьте свой номер телефона, чтобы зарегистрироваться.',
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

    await message.answer(
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

    await state.set_state(RegistrationState.address)
    await msg.answer(
        'Введите свой адрес (квартиру вводить необязательно).\n'
        'Пример: Москва, ул. Победы, д. 25, кв. 10\n\n'
        '* Даже если у вас не улица, а переулок/проспект, '
        'все равно пишите ул.',
    )


@router.message(F.text, StateFilter(RegistrationState.address))
async def set_address(msg: Message, state: FSMContext):
    matches = re.search(
        r'([А-ЯЁ\s\-]+)(?:,\s*)?ул\.?([А-ЯЁ\s\-\.\d]+)(?:,\s*)?'
        r'д\.?\s*([А-ЯЁ\d/]+)(?:,\s*)?(?:кв\.?)?\s*(\d+)?',
        msg.text,
        re.IGNORECASE,
    )

    if not matches:
        await msg.answer('Вы ввели некорректный адрес. Попробуйте еще раз.')
        return

    registered_city, street, house, appartment = matches.groups()
    if not registered_city.strip() or not street.strip() or not house:
        await msg.answer('Вы ввели некорректный адрес. Попробуйте еще раз.')
        return

    await state.update_data(
        registered_city=registered_city.strip(),
        street=street.strip(),
        house=house,
        appartment=appartment,
    )

    await state.set_state(RegistrationState.nationality)
    await msg.answer(
        'Введите свое гражданство.\nПример: Россия',
    )


@router.message(F.text, StateFilter(RegistrationState.nationality))
async def set_nationality(msg: Message, state: FSMContext):
    await state.update_data(nationality=msg.text)
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
        await msg.answer(
            'Вы перешли в главное меню',
            reply_markup=menu_kb,
        )
    else:
        await msg.answer('К сожалению, во время регистрации произошла ошибка.')

    await state.clear()


@router.callback_query(F.data == 'to_menu')
async def to_menu(query: CallbackQuery, state: FSMContext):
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
