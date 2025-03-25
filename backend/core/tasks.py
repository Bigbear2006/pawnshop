import asyncio

import magic
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import BufferedInputFile
from celery import shared_task
from celery.utils.log import get_task_logger

from bot.loader import bot
from core.models import Client

task_logger = get_task_logger(__name__)


def handle_send_message_errors(send_message_func):
    async def decorator(chat_id: int):
        try:
            await send_message_func(chat_id)
        except TelegramRetryAfter as e:
            task_logger.info(
                f'Cannot send a message to user (id={chat_id}) '
                f'because of rate limit',
            )
            await asyncio.sleep(e.retry_after)
            await send_message_func(chat_id)
        except TelegramBadRequest as e:
            task_logger.info(
                f'Cannot send a message to user (id={chat_id}) '
                f'because of an {e.__class__.__name__} error: {str(e)}',
            )

    return decorator


@shared_task
def send_publication(text: str, media_url: str = None):
    async def main():
        @handle_send_message_errors
        async def send_message(chat_id: int):
            if media_url:
                media_type = magic.from_file(media_url, mime=True)
                media = BufferedInputFile.from_file(media_url)
            else:
                media_type = ''
                media = None

            if media_type.startswith('image/'):
                await bot.send_photo(
                    chat_id,
                    media,
                    caption=text,
                )
            elif media_type.startswith('video/'):
                await bot.send_video(
                    chat_id,
                    media,
                    caption=text,
                )
            else:
                await bot.send_message(chat_id, text)

        await asyncio.wait(
            [
                asyncio.create_task(send_message(client.pk))
                async for client in Client.objects.all()
            ],
        )

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
