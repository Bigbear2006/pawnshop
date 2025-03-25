import re
from dataclasses import dataclass, field

from environs import Env

env = Env()
env.read_env()


def load_access_token():
    try:
        with open('token.txt', encoding='utf-8') as f:
            token = f.read()
    except FileNotFoundError:
        with open('token.txt', 'w', encoding='utf-8') as _:
            token = ''
    return token


@dataclass
class Settings:
    BOT_TOKEN: str = field(default_factory=lambda: env('BOT_TOKEN'))
    REDIS_URL: str = field(default_factory=lambda: env('REDIS_URL'))

    SMART_LOMBARD_ACCOUNT_ID: int = field(
        default_factory=lambda: env('SMART_LOMBARD_ACCOUNT_ID'),
    )
    SMART_LOMBARD_SECRET_KEY: str = field(
        default_factory=lambda: env('SMART_LOMBARD_SECRET_KEY'),
    )
    SMART_LOMBARD_ACCESS_TOKEN: str = field(default_factory=load_access_token)
    SMART_LOMBARD_BASE_URL: str = field(
        default='https://online.smartlombard.ru/api/exchange/v1/',
    )

    FORWARD_CHAT_ID: str = field(default='-1002309981972')
    SITE_URL: str = field(default_factory=lambda: 'https://google.com/')
    AUTOLOAN_SITE_URL: str = field(
        default_factory=lambda: 'https://google.com/',
    )
    VK_URL: str = field(default_factory=lambda: 'https://vk.com/')
    TG_URL: str = field(default_factory=lambda: 'https://t.me/search_net_bot')

    PHONE_REGEXP: re.Pattern = field(default=re.compile('[^0-9]+'))


settings = Settings()
