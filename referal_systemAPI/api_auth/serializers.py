from rest_framework import serializers

from app_users.models import User


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Сериализатор ввода пользователем номера телефона."""

    class Meta:
        model = User
        fields = [
            "phone_number",
        ]


class VerificationNumberSerializer(serializers.Serializer):
    """Сериализатор ввода проверочного кода."""

    number = serializers.IntegerField(max_value=9999, label="Проверочный код")
