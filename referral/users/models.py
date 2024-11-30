from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(
        'Номер телефона', max_length=12, unique=True
    )
    invite_code = models.CharField(
        'Инвайт-код', max_length=6, unique=True
    )
    referred_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='referrals',
        verbose_name='Активация инвайт-кода'
    )
    is_admin = models.BooleanField('Администратор', default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin
