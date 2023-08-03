from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from app_users.models import User
from .serializers import ProfileUserSerializer, InviteCodeSerializer


class GetProfileUserAPIView(generics.ListAPIView):
    """
    API запрос на профиль пользователя.
    В профиле отображается список пользователей с введённым инфвайт-кодом текущего.
    """

    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class SetSomeoneInviteCodeApiView(generics.UpdateAPIView):
    """
    В профиле есть возможность ввести чужой инвайт-код,
    если он был введён раннее, то сохранение не будет.
    """
    serializer_class = InviteCodeSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.get_queryset().get()
            referral = request.data["someone_invite_code"]
            list_referral = (
                User.objects.only("your_invite_code")
                .all()
                .values_list("your_invite_code", flat=True)
            )
            if user.someone_invite_code is None:
                if referral in list_referral:
                    user.someone_invite_code = referral
                    user.save()
                    return Response(
                        {"msg": f"Добавлен реферал с номером {referral}"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"msg": "Такого пользователя не существует."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"msg": "Реферал уже добавлен."}, status=status.HTTP_400_BAD_REQUEST
            )
