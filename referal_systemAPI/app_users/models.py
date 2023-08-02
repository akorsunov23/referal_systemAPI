import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .manager import CustomUserManager

phone_validate = RegexValidator(
    regex=r'^8\d{10}$',
    message='Номер телефона должен быть введен в '
            'формате: "81234567890". '
            'Максимальная длина 11 символов.'
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = None
    password = None
    phone_number = models.CharField(
        unique=True,
        max_length=11,
        validators=[phone_validate],
        verbose_name='номер телефона',
        blank=True, null=True
    )
    code = models.IntegerField(
        verbose_name='Проверочный код'
    )
    your_invite_code = models.CharField(
        unique=True,
        max_length=6,
        verbose_name='инвайт-код'
    )
    someone_invite_code = models.CharField(
        max_length=6,
        verbose_name='чужой инвайт-код',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        """При добавлении нового пользователя генерируется личный инвайт-код"""
        if not self.pk:
            self.your_invite_code = None
            list_invite_code = (
                User.objects
                .only('your_invite_code')
                .all()
                .values_list('your_invite_code', flat=True)
            )
            while not self.your_invite_code:
                your_invite_code = ''.join(
                    random.choices(
                        string.ascii_uppercase + string.digits,
                        k=6
                    )
                )
                if your_invite_code not in list_invite_code:
                    self.your_invite_code = your_invite_code
                    return super().save()
        return super().save()
