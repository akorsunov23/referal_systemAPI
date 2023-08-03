from django.urls import path
from .api import GetProfileUserAPIView, SetSomeoneInviteCodeApiView

app_name = "api_users"

urlpatterns = [
    path("profile/", GetProfileUserAPIView.as_view(), name="profile_user"),
    path("profile/<int:pk>/set_invite_code/", SetSomeoneInviteCodeApiView.as_view(), name="set_invite_code")
]
