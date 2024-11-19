from django.contrib.auth.views import LogoutView
from django.urls import path, include

from petstagram.accounts import views

urlpatterns = [
    path("register/", views.Register.as_view(), name="accounts-register"),
    path("login/", views.AppUserLogin.as_view(), name="accounts-login"),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
    path("profile/<int:pk>/", include([
        path("", views.ProfileDetails.as_view(), name="profile-details"),
        path("edit/", views.EditProfile.as_view(), name="edit-profile"),
        path("delete/", views.DeleteProfile.as_view(), name="delete-profile"),
    ]))
]