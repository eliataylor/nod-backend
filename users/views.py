from django.shortcuts import render
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from rest_framework import filters, status
from rest_framework.response import Response

from utils.helpers import decrypt
from nod_backend.settings import GOOGLE_CALLBACK_URL

from .helpers import (
    check_if_domain_allowed,
    notify_admin_that_user_wanted_to_signup
)
from .models import User
from .serializers import (
    CustomPasswordChangeSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomSocialLoginSerializer,
    UserSerializer,
)


# Create your views here.


class LimitedRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        user_email = self.request.data.get("email")
        if check_if_domain_allowed(user_email):
            return super().create(request, *args, **kwargs)
        notify_admin_that_user_wanted_to_signup(user_email)
        return Response(
            {"domain": ["Users with such a domain can't be registered or authorized"]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LimitedLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        user_email = self.serializer.data.get("email")
        if not check_if_domain_allowed(user_email):
            notify_admin_that_user_wanted_to_signup(user_email)
            return Response(
                {"domain": ["Sorry, users with such a domain can't log in anymore"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.serializer.validated_data["user"]

        self.login()
        return self.get_response()


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = GOOGLE_CALLBACK_URL
    serializer_class = CustomSocialLoginSerializer