from rest_framework import serializers

from app_users.models import User


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор отдачи данных для профиля пользователя."""
    referral_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'pk', 'phone_number', 'your_invite_code', 'someone_invite_code', 'referral_list'
        ]
        read_only_fields = ['pk', 'phone_number', 'your_invite_code', 'referral_list']

    @staticmethod
    def get_referral_list(obj):
        return (User.objects
                .filter(someone_invite_code=obj.your_invite_code)
                .values_list('phone_number', flat=True))


class InviteCodeSerializer(serializers.Serializer):
    """Сериализатор ввода инвайт кода."""
    someone_invite_code = serializers.CharField(max_length=6)
