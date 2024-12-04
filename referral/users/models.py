from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumbers import is_valid_number, parse

from .managers import UserManager
from .utils import generate_invite_code


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=12, unique=True)
    invite_code = models.CharField(
        max_length=6, unique=True, default=generate_invite_code
    )
    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals'
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone_number

    @staticmethod
    def validate_phone_number(phone_number):
        try:
            parsed_phone = parse(phone_number)
            return is_valid_number(parsed_phone)
        except Exception:
            return False
