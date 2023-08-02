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

    code = serializers.IntegerField(
        max_value=9999, min_value=1000, label="Проверочный код"
    )
