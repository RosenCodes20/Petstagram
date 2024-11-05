from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_image_size


class Photo(models.Model):

    photo = models.ImageField(validators=[
        validate_image_size
    ])

    description = models.TextField(
        max_length=300,
        validators=[
            MinLengthValidator(10)
        ],
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=30
    )

    tagged_pets = models.ManyToManyField(
        to=Pet,
        related_name="tagged_pets",
        null=True,
        blank=True
    )

    date_of_publication = models.DateField(
        auto_now_add=True
    )