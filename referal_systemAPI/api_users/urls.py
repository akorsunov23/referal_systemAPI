from django.urls import path
from .api import GetProfileUserAPIView
app_name = 'api_users'

urlpatterns = [
    path('profile/', GetProfileUserAPIView.as_view(), name='profile_user')
]
