from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from app_users.models import User


class ProfileUser(SuccessMessageMixin, LoginRequiredMixin, View):
    """Профиль пользователя."""

    template_name = "app_user/user_profile.html"
    success_url = reverse_lazy("app_users:user_profile")

    def get(self, request, *args, **kwargs):
        referral_list = (
            User.objects.only(
                "phone_number",
            )
            .filter(someone_invite_code=self.request.user.your_invite_code)
            .all()
        )
        context = {
            "referral_list": referral_list,
        }
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        someone_invite_code = self.request.POST.get("someone_invite_code")
        list_invite_code = (
            User.objects.only("your_invite_code")
            .all()
            .values_list("your_invite_code", flat=True)
        )
        if someone_invite_code in list_invite_code:
            self.request.user.someone_invite_code = someone_invite_code
            self.request.user.save()
            messages.add_message(
                self.request, messages.INFO, "Чужой инвайт код сохранён."
            )
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            self.request, messages.INFO, "Такого пользователя не существует."
        )
        return HttpResponseRedirect(self.success_url)
