from django import forms
from django.forms import TextInput, DateTimeInput

from petstagram.pets.models import Pet


class PetBaseForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ["name", "date_of_birth", "pet_photo"]

        labels = {
            "name": "Pet name:",
            "date_of_birth": "Date of birth:",
            "pet_photo": "Link to image:"
        }

        widgets = {
            "name": TextInput(attrs={"placeholder": "Pet name"}),
            "pet_photo": TextInput(attrs={"placeholder": "Link to image"}),
            "date_of_birth": TextInput(attrs={"type": "date"})
        }


class PetCreateForm(PetBaseForm):
    pass


class PetEditForm(PetBaseForm):
    pass


class PetDeleteForm(PetBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True
            self.fields[field].widget.attrs["readonly"] = "readonly"