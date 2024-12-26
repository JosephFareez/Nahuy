from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/telegram/", views.telegram_login, name="telegram_login"),
    path("user-profile/", views.user_profile, name="user_profile"),
]
