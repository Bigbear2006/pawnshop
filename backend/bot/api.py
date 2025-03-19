from aiohttp import ClientSession

from bot.loader import logger
from bot.settings import settings


class SmartLombardAPI:
    @staticmethod
    def get_headers() -> dict:
        return {
            'Authorization': f'Bearer {settings.SMART_LOMBARD_ACCESS_TOKEN}',
        }

    @staticmethod
    async def login() -> dict:
        async with ClientSession(settings.SMART_LOMBARD_BASE_URL) as session:
            data = {
                'account_id': settings.SMART_LOMBARD_ACCOUNT_ID,
                'secret_key': settings.SMART_LOMBARD_SECRET_KEY,
            }
            async with session.post('auth/access_token', data=data) as rsp:
                data = await rsp.json()
                logger.info(data)
                return data

    @staticmethod
    async def get_client_by_phone(phone: str) -> dict | None:
        async with ClientSession(settings.SMART_LOMBARD_BASE_URL) as session:
            async with session.get(
                    'clients/natural_persons/',
                    headers=SmartLombardAPI.get_headers(),
                    params={'phone': phone}
            ) as rsp:
                data = await rsp.json()
                logger.info(data)

                if not data['status']:
                    return None

                client = data['result']['clients_natural_persons'][0]
                return client if (
                        settings.PHONE_REGEXP.sub('', client['phone'])
                        == settings.PHONE_REGEXP.sub('', phone)
                ) else None

    @staticmethod
    async def get_client(client_id: int | str) -> dict | None:
        async with ClientSession(settings.SMART_LOMBARD_BASE_URL) as session:
            async with session.get(
                    f'clients/natural_persons/{client_id}',
                    headers=SmartLombardAPI.get_headers(),
            ) as rsp:
                data = await rsp.json()
                logger.info(data)

                if not data['status']:
                    return None

                return data['result']['client_natural_person']
