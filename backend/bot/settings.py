from dataclasses import dataclass, field

from environs import Env

env = Env()
env.read_env()


@dataclass
class Settings:
    BOT_TOKEN: str = field(default_factory=lambda: env('BOT_TOKEN'))
    REDIS_URL: str = field(default_factory=lambda: env('REDIS_URL'))

    SITE_URL: str = field(default_factory=lambda: 'https://google.com/')
    VK_URL: str = field(default_factory=lambda: 'https://vk.com/')
    TG_URL: str = field(default_factory=lambda: 'https://t.me/search_net_bot')


settings = Settings()
