from django.contrib.auth import get_user_model
from django.db import models

from petstagram.accounts.models import AppUser

UserModel = get_user_model()

class Profile(models.Model):

    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    profile_picture = models.URLField(
        null=True,
        blank=True
    )

    def get_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name or self.last_name or "Anonymous"