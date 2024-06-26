from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import LogoutView, PasswordResetView
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    LimitedLoginView,
    LimitedRegisterView, GoogleLogin,
)

app_name = "users"

urlpatterns = [
    path("register/", LimitedRegisterView.as_view(), name="account_signup"),
    path("login/", LimitedLoginView.as_view(), name="rest_login"),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        TemplateView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'account-email-verification-sent/',
        TemplateView.as_view(),
        name='account_email_verification_sent',
    ),
]
