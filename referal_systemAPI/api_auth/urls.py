from django.urls import path

from .api import GetPhoneNumberUserAPIView, VerificationNumberAPI

app_name = "api_auth"

urlpatterns = [
    path("", GetPhoneNumberUserAPIView.as_view(), name="get_phone_number"),
    path("<str:phone_number>/verification_code/", VerificationNumberAPI.as_view(), name="get_verification_code"),
]
