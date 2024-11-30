import random
import string

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def make_random_invite_code(self):
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

    def create_user(
        self, phone_number, password=None, **extra_fields
    ):
        if not phone_number:
            raise ValueError('Поле `номер телефона` не должно быть пустым')

        invite_code = self.make_random_invite_code()
        user = self.model(
            phone_number=phone_number, invite_code=invite_code, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None):
        invite_code = self.make_random_invite_code()
        user = self.create_user(
            phone_number=phone_number, invite_code=invite_code
        )
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user
