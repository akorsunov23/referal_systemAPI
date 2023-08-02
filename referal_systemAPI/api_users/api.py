from rest_framework import generics, status
from rest_framework.response import Response

from app_users.models import User
from .serializers import ProfileUserSerializer, InviteCodeSerializer


class GetProfileUserAPIView(generics.ListAPIView):
    """Запрос на профиль пользователя."""

    serializer_class = ProfileUserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs["pk"])

    def put(self, request):
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
