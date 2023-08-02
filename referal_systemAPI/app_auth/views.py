import random

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View

from api_auth.services import send_sms
from app_users.models import User
from .forms import VerificationCodeForms, PhoneNumberForms


class CreateOfUpdateUserView(SuccessMessageMixin, View):
    """Представление для запроса номера телефона и добавление его в бд."""

    template_name = "app_auth/get_phone_number.html"

    def get_success_url(self):
        return reverse(
            "app_auth:auth_user",
            kwargs={"phone_number": self.request.POST.get("phone_number")},
        )

    def get(self, request, *args, **kwargs):
        context = {
            "form": PhoneNumberForms,
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        code = random.randint(1000, 9999)
        phone_number = self.request.POST.get("phone_number")
        odj, create = User.objects.update_or_create(
            phone_number=phone_number,
            defaults={"phone_number": phone_number, "code": code},
        )
        response = send_sms(code=odj.code, phones=odj.phone_number)
        if response:
            messages.add_message(
                self.request,
                messages.INFO,
                "СМС с кодом отправлено на указанный номер.",
            )
            return HttpResponseRedirect(self.get_success_url())
        messages.add_message(
            self.request, messages.INFO, "Произошла ошибка, попробуйте позже."
        )
        return HttpResponseRedirect(reverse("app_auth:get_phone"))


class AuthUser(SuccessMessageMixin, View):
    """Проверка кода и аутентификация пользователя."""

    template_name = "app_auth/get_verification_number.html"
    form = VerificationCodeForms
    success_url = reverse_lazy("app_users:user_profile")

    def get(self, request, *args, **kwargs):
        context = {"form": self.form}
        return render(request, self.template_name, context)

    def get_object(self):
        return User.objects.get(phone_number=self.kwargs["phone_number"])

    def post(self, request, *args, **kwargs):
        code = int(self.request.POST.get("code"))
        if self.get_object().code == code:
            login(self.request, self.get_object())
            return HttpResponseRedirect(self.success_url)
        messages.add_message(self.request, messages.INFO, "Не верный код")
        return HttpResponseRedirect(
            reverse(
                "app_auth:auth_user",
                kwargs={"phone_number": self.kwargs["phone_number"]},
            )
        )
