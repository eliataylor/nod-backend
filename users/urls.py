from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import LogoutView, PasswordResetView
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    LimitedLoginView,
    LimitedRegisterView,
)

app_name = "users"

urlpatterns = [
    path("register/", LimitedRegisterView.as_view(), name="account_signup"),
    path("login/", LimitedLoginView.as_view(), name="rest_login"),
]
