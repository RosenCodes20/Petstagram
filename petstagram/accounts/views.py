from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import UserRegistrationForm, ProfileEditForm
from petstagram.accounts.models import AppUser, Profile

user_model = get_user_model()
class AppUserLogin(LoginView):
    template_name = "accounts/login-page.html"

    # def form_valid(self, form):
    #     super().form_valid(form)
    #
    #     profile, _ = Profile.objects.get_or_create(user=self.request.user)
    #
    #     return HttpResponseRedirect(self.get_success_url())

class DeleteProfile(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = AppUser
    template_name = "accounts/profile-delete-page.html"
    success_url = reverse_lazy("home-page")

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

class ProfileDetails(DetailView, LoginRequiredMixin):
    model = AppUser
    template_name = "accounts/profile-details-page.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        photos_with_likes = self.object.photo_set.annotate(likes_count=Count("like"))

        context["total_likes_count"] = sum(photo.likes_count for photo in photos_with_likes)
        context["total_pets_count"] = self.object.pet_set.count()
        context["total_photos_count"] = self.object.photo_set.count()

        return context

class EditProfile(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile-edit-page.html"

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):

        return reverse_lazy(
            "profile-details",
            kwargs={
                "pk": self.object.pk
            }
        )


class Register(CreateView):
    model = user_model
    form_class = UserRegistrationForm
    template_name = "accounts/register-page.html"
    success_url = reverse_lazy("home-page")