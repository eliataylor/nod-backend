from django.db import models

import hashlib

from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from utils.models import BumpParentsModelMixin, TimedModel


# Create your models here.


class User(AbstractUser, BumpParentsModelMixin):
    """
    Add additional fields to the user model here.
    """

    avatar = models.FileField(upload_to="profile-pictures/", blank=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    timezone = models.CharField(default="America/New_York", max_length=64)
    updated_at = models.DateTimeField(
        db_index=True,
        auto_now=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.get_full_name()} <{self.email or self.username}>"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_display_name(self) -> str:
        if self.get_full_name().strip():
            return self.get_full_name()
        return self.email or self.username

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        return "https://www.gravatar.com/avatar/{}?s=128&d=identicon".format(self.gravatar_id)

    @property
    def gravatar_id(self) -> str:
        # https://en.gravatar.com/site/implement/hash/
        return hashlib.md5(self.email.lower().strip().encode("utf-8")).hexdigest()

    def add_email_address(self, request, new_email):
        # Add a new email address for the user, and send email confirmation.
        # Old email will remain the primary until the new one is confirmed.
        return EmailAddress.objects.add_email(request, request.user, new_email, confirm=True)

    @receiver(email_confirmed)
    def update_user_email(sender, request, email_address, **kwargs):
        # Once the email address is confirmed, make new email_address primary.
        # This also sets user.email to the new email address.
        # email_address is an instance of allauth.account.models.EmailAddress
        email_address.set_as_primary()
        # Get rid of old email addresses
        EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()


class AvailableDomain(TimedModel):
    name = models.CharField(max_length=64)
