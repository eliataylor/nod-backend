from allauth.socialaccount.helpers import complete_social_login
from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    SocialLoginSerializer,
)
from dj_rest_auth.serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.utils.translation import gettext_lazy as _
from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .forms import CustomResetForm
from .helpers import check_if_domain_allowed, notify_admin_that_user_wanted_to_signup
from .models import User


class UserRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name", "")
        data_dict["last_name"] = self.validated_data.get("last_name", "")
        return data_dict


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["user_permissions", "groups", "password"]


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    @property
    def password_reset_form_class(self):
        return CustomResetForm


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def save(self):
        if self.user and self.validated_data.get("new_password1"):
            self.user.set_password(self.validated_data["new_password1"])
            self.user.save()

        return self.user


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    def save(self):
        user = self.context["request"].user  # Get the user from request context

        if user and self.validated_data.get("new_password1"):
            user.set_password(self.validated_data["new_password1"])
            user.save()

        return user


class CustomLoginSerializer(LoginSerializer):
    """
    Customize validation methods.
    If user added a new email address and not verify it, do not allow login with it
    """

    @staticmethod
    def validate_email_verification_status(user, email):
        from allauth.account import app_settings

        if (
            app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(email=email, verified=True).exists()
        ):
            raise serializers.ValidationError(_("E-mail is not verified."))

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if "dj_rest_auth.registration" in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email)

        attrs["user"] = user
        return attrs


class CustomSocialLoginSerializer(SocialLoginSerializer):
    """
    Check the domain before creating a Google account
    Do not raise an exception, if user already signed up in a different flow
    with the same email address
    """

    def check_domain(self, login):
        # Custom Login
        # If user's domain not in the available list of domains,
        # then raise an exception
        user_email = login.user.email
        if not check_if_domain_allowed(user_email):
            notify_admin_that_user_wanted_to_signup(user_email)
            raise serializers.ValidationError({"domain": "Users with such a domain can't be registered or authorized"})

    def validate(self, attrs):
        view = self.context.get("view")
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable"),
            )

        adapter_class = getattr(view, "adapter_class", None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().app

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        access_token = attrs.get("access_token")
        code = attrs.get("code")
        # Case 1: We received the access_token
        if access_token:
            tokens_to_parse = {"access_token": access_token}
            token = access_token
            # For sign in with apple
            id_token = attrs.get("id_token")
            if id_token:
                tokens_to_parse["id_token"] = id_token

        # Case 2: We received the authorization code
        elif code:
            self.set_callback_url(view=view, adapter_class=adapter_class)
            self.client_class = getattr(view, "client_class", None)

            if not self.client_class:
                raise serializers.ValidationError(
                    _("Define client_class in view"),
                )

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth,
            )
            token = client.get_access_token(code)
            access_token = token["access_token"]
            tokens_to_parse = {"access_token": access_token}

            # If available we add additional data to the dictionary
            for key in ["refresh_token", "id_token", adapter.expires_in_key]:
                if key in token:
                    tokens_to_parse[key] = token[key]
        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token or code is required."),
            )

        social_token = adapter.parse_token(tokens_to_parse)
        social_token.app = app

        try:
            if adapter.provider_id == "google":
                login = self.get_social_login(adapter, app, social_token, response={"access_token": token})
            else:
                login = self.get_social_login(adapter, app, social_token, token)
            self.check_domain(login)
            ret = complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_("Incorrect value"))

        if isinstance(ret, HttpResponseBadRequest):
            raise serializers.ValidationError(ret.content)

        if not login.is_existing:
            # If we have an account already signed up in a different flow
            # with the same email address, we do not raise an exception.
            # We return an existing user

            account_exists = (
                get_user_model()
                .objects.filter(
                    email=login.user.email,
                )
                .exists()
            )
            if account_exists:
                attrs["user"] = (
                    get_user_model()
                    .objects.filter(
                        email=login.user.email,
                    )
                    .first()
                )

                return attrs

            login.lookup()
            login.save(request, connect=True)
            self.post_signup(login, attrs)

        attrs["user"] = login.account.user
        return attrs


    @staticmethod
    def change_user_password(user, new_password):
        if user and user.pk and new_password:
            user.set_password(new_password)
            user.save()

        return user
