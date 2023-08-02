from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер кастомной модели User.
    """
    def create_user(self, phone_number, code, **extra_fields):
        """Добавление обычного пользователя."""
        if not phone_number:
            raise ValueError('Не указан номер телефона')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(code)
        user.save()
        return user

    def create_superuser(self, phone_number, code, **extra_fields):
        """Добавление суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должно быть is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self.create_user(phone_number, code, **extra_fields)
