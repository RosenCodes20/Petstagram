from django.db import models

from petstagram.accounts.models import AppUser
from petstagram.photos.models import Photo


class Comment(models.Model):

    comment_text = models.TextField(
        max_length=300
    )

    date_time_of_publication = models.DateTimeField(
        auto_now_add=True
    )

    photo = models.ForeignKey(
        to=Photo,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    user = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-date_time_of_publication"]

class Like(models.Model):

    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE
    )
