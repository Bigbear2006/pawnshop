import os

import django
from aiogram import F
from aiogram.enums import ChatType
from aiogram.types import BotCommand

from bot.api import refresh_access_token
from bot.loader import bot, dp, logger, loop
from bot.settings import settings


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
    dp.message.filter(F.chat.type == ChatType.PRIVATE)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        [
            BotCommand(command='/start', description='Запустить бота'),
        ],
    )

    logger.info('Starting bot...')
    logger.info(
        f'Smartlombard access_token={settings.SMART_LOMBARD_ACCESS_TOKEN}',
    )
    loop.create_task(refresh_access_token())
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop.run_until_complete(main())
