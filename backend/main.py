import asyncio
import os

import django
from aiogram import F
from aiogram.types import BotCommand

from bot.loader import bot, dp, logger


async def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

    from bot.handlers import (
        bonus_balance,
        branches,
        commands,
        online_evaluation,
        social_media,
    )

    dp.include_routers(
        commands.router,
        bonus_balance.router,
        branches.router,
        online_evaluation.router,
        social_media.router,
    )
    dp.message.filter(F.chat.type == 'private')

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        [
            BotCommand(command='/start', description='Запустить бота'),
        ],
    )

    logger.info('Starting bot...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
