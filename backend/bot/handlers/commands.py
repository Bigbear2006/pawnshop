from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!')
