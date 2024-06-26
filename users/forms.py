from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.forms import AllAuthPasswordResetForm

from nod_backend.settings import ACCOUNT_PASSWORD_RESET_URL


class CustomResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            uid = user_pk_to_url_str(user)

            context = {
                "user": user,
                "password_reset_url": f"{ACCOUNT_PASSWORD_RESET_URL}?uid={uid}&key={temp_key}",
            }
            get_adapter(request).send_mail("account/email/password_reset_key", email, context)
        return self.cleaned_data["email"]
