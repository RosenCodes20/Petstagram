from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import TextInput

from petstagram.accounts.models import AppUser, Profile

user_model = get_user_model()

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ["email"]
        model = user_model

# #
# class UserLoginForm(AuthenticationForm):
#     username = forms.EmailField(widget=TextInput(attrs={"autofocus": True}))
#
#     password = forms.CharField(
#         label=("Password",),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
#     )

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ("user", )

        labels = {
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "date_of_birth": "Date Of Birth:",
            "profile_picture": "Profile Picture:"
        }