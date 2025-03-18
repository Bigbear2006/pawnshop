from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.keyboards.inline import menu_kb
from bot.keyboards.reply import request_contact_kb

router = Router()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer(
        'Отправьте свой номер телефона, чтобы зарегистрироваться.',
        reply_markup=request_contact_kb,
    )


@router.message(F.contact)
async def auth(msg: Message):
    message = await msg.answer(
        'Вы успешно авторизовались по номеру телефона.',
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        f'Привет, {msg.from_user.full_name}!\n',
        reply_markup=menu_kb,
    )


@router.callback_query(F.data == 'switch_to_menu_kb')
async def switch_to_menu_kb(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(
        'Главное меню',
        reply_markup=menu_kb,
    )
