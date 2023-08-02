from django.urls import path

from .views import CreateOfUpdateUserView, AuthUser

app_name = "app_auth"

urlpatterns = [
    path("", CreateOfUpdateUserView.as_view(), name="get_phone"),
    path("<str:phone_number>/verification_code/", AuthUser.as_view(), name="auth_user"),
]
