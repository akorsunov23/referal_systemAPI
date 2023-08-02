from django.contrib.auth.forms import forms

from app_users.models import User


class PhoneNumberForms(forms.ModelForm):
    """Форма для запроса номера телефона."""

    class Meta:
        model = User
        fields = [
            "phone_number",
        ]


class VerificationCodeForms(forms.Form):
    """Форма для запроса проверочного кода."""

    code = forms.IntegerField(max_value=9999, min_value=1000, label="Проверочный код")
