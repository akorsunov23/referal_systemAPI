import random

from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response

from app_users.models import User
from .serializers import PhoneNumberSerializer, VerificationNumberSerializer
from .services import send_sms


class GetPhoneNumberUserAPIView(generics.CreateAPIView):
    """Представление запроса номера пользователя и сохранение его с кодом проверки."""

    serializer_class = PhoneNumberSerializer
    queryset = User.objects.all()
    code = random.randint(1000, 9999)
    success_response = Response(
        {"msg": "СМС с кодом отправлено на телефон"}, status=status.HTTP_200_OK
    )
    not_success_response = Response(
        {
            "msg": "Произошла ошибка при отправки СМС. "
            "Пожалуйста, проверьте номер телефона и повторите позже."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    def perform_create(self, serializer):
        serializer.save(code=self.code)

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            phone_number = request.data["phone_number"]
            answer = send_sms(phones=phone_number, code=self.code)
            if answer:
                return self.success_response
            return self.not_success_response
        except Exception as ex:
            if (
                "пользователь с таким номер телефона уже существует."
                == ex.args[0]["phone_number"][0]
            ):
                phone_number = request.data["phone_number"]
                User.objects.filter(phone_number=phone_number).update(code=self.code)
                answer = send_sms(phones=phone_number, code=self.code)
                if answer:
                    return self.success_response
                return self.not_success_response
            raise ex


class VerificationNumberAPI(generics.GenericAPIView):
    """Ввод проверочного кода и аутентификация пользователя."""

    serializer_class = VerificationNumberSerializer

    def get_queryset(self):
        return User.objects.get(phone_number=self.kwargs["phone_number"])

    def post(self, request, phone_number):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = int(request.data["code"])
            user = self.get_queryset()
            if user.code == code:
                login(self.request, user)
                return Response(
                    {"msg": f"Пользователь {user} аутентифицирован."},
                    status=status.HTTP_200_OK,
                    headers=login(self.request, user),
                )
            return Response(
                {"msg": f"Код не верный"}, status=status.HTTP_401_UNAUTHORIZED
            )
