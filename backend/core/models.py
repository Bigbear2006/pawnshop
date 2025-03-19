from aiogram import types
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class User(AbstractUser):
    pass


class ClientManager(models.Manager):
    async def from_tg_user(self, user: types.User) -> 'Client':
        return await self.acreate(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_premium=user.is_premium or False,
        )

    async def update_from_tg_user(self, user: types.User) -> None:
        await self.filter(pk=user.id).aupdate(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_premium=user.is_premium or False,
        )

    async def create_or_update_from_tg_user(
        self,
        user: types.User,
    ) -> tuple['Client', bool]:
        try:
            client = await self.aget(pk=user.id)
            await self.update_from_tg_user(user)
            await client.arefresh_from_db()
            return client, False
        except ObjectDoesNotExist:
            return await self.from_tg_user(user), True


class Client(models.Model):
    id = models.PositiveBigIntegerField(
        'Телеграм ID',
        primary_key=True,
    )
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField(
        'Фамилия',
        max_length=255,
        null=True,
        blank=True,
    )
    username = models.CharField(
        'Ник',
        max_length=32,
        null=True,
        blank=True,
    )
    is_premium = models.BooleanField(
        'Есть премиум',
        default=False,
    )
    phone = models.CharField(
        'Номер телефона',
        max_length=100,
        null=True,
        blank=True,
    )
    smart_lombard_id = models.BigIntegerField(
        'ID пользователя в smartlombard',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    objects = ClientManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        username = self.first_name
        if self.username:
            username += f' (@{self.username})'
        return username


class Branch(models.Model):
    title = models.CharField('Название', max_length=255)
    work_schedule = models.CharField('График работы', max_length=255)
    manager_url = models.URLField('Ссылка на менеджера')
    objects: models.Manager

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'
        ordering = ['-title']

    def __str__(self):
        return self.title[:25]


class SpendOption(models.Model):
    text = models.TextField('Текст')
    objects: models.Manager

    class Meta:
        verbose_name = 'На что потратить'
        verbose_name_plural = 'На что потратить'
        ordering = ['id']

    def __str__(self):
        return self.text[:50]


class OnlineEvaluationGuide(models.Model):
    text = models.TextField('Инструкция')
    objects: models.Manager

    class Meta:
        verbose_name = 'Инструкция по онлайн оценке'
        verbose_name_plural = 'Инструкция по онлайн оценке'
        ordering = ['id']

    def __str__(self):
        return self.text[:50]


class Publication(models.Model):
    text = models.TextField('Текст')
    media = models.FileField(
        'Фото или видео',
        upload_to='publications',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    objects: models.Manager

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:100]
