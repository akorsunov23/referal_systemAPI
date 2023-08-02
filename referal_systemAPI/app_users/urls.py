from django.urls import path

from .views import ProfileUser

app_name = "app_users"

urlpatterns = [
    path("profile/", ProfileUser.as_view(), name="user_profile"),
]
