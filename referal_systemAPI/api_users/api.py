from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status
from rest_framework.response import Response

from app_users.models import User
from .serializers import ProfileUserSerializer, InviteCodeSerializer


class GetProfileUserAPIView(LoginRequiredMixin, generics.ListAPIView):
    """Запрос на профиль пользователя."""
    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def put(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.get_queryset().get()
            referral = request.data['someone_invite_code']
            if user.someone_invite_code is None:
                user.someone_invite_code = referral
                user.save()
                return Response(
                    {
                        'msg': f'Добавлен реферал с номером {referral}'
                    }
                )
            return Response(
                    {
                        'msg': f'Реферал уже добавлен.'
                    }
                )

