from django import forms

from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):

    class Meta:
        model = Photo
        exclude = ("date_of_publication", "user")


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):

    class Meta(PhotoBaseForm.Meta):
        exclude = ("date_of_publication", "photo", "user")