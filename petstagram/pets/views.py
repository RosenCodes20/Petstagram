from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import PermissionsMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


class AddPetPage(CreateView, LoginRequiredMixin):
    model = Pet
    form_class = PetCreateForm
    template_name = "pets/pet-add-page.html"

    def form_valid(self, form):
        pet = form.save(commit=False)

        pet.user = self.request.user

        pet.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "profile-details",
            kwargs={
                "pk": self.request.user.pk
            }
        )

# def add_page(request):
#
#     form = PetCreateForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("profile-details", pk=1)
#
#
#     context = {
#         "form": form
#     }
#
#     return render(request, "pets/pet-add-page.html", context)

@login_required
def delete_page(request, username, pets_slug):

    pet = Pet.objects.get(slug=pets_slug)

    form = PetDeleteForm(request.POST or None, instance=pet)

    if request.method == "POST":
        if form.is_valid():
            pet.delete()
            if not request.user.is_superuser:
                return redirect("profile-details", pk=request.user.pk)

    context = {
        "pet": pet,
        "form": form
    }

    return render(request, "pets/pet-delete-page.html", context)


class PetDetailsPage(DetailView, LoginRequiredMixin):
    model = Pet
    template_name = "pets/pet-details-page.html"
    context_object_name = "pet"
    slug_url_kwarg = "pets_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["photos"] = self.object.tagged_pets.all()
        context["comments"] = CommentForm

        for photo in context["photos"]:
            photo.has_liked = photo.like_set.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False


        return context

# def details_page(request, username, pets_slug):
#
#     pet = Pet.objects.get(slug=pets_slug)
#     photos = Photo.objects.all()
#
#     context = {
#         "pet": pet,
#         "photos": photos
#     }
#
#     return render(request, "pets/pet-details-page.html", context)

#TODO: FINISH THE URL ATTACKS (NOT TOMORROW OR I WILL BE ASLEEP AT THE FIRST HOUR (GOOD NIGHT) :)  )

class EditPetPage(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Pet
    form_class = PetEditForm
    template_name = "pets/pet-edit-page.html"
    slug_url_kwarg = "pets_slug"
    context_object_name = "pet"

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_success_url(self):
        return reverse_lazy(
            "details-page",
            kwargs={
                "username": self.kwargs["username"],
                "pets_slug": self.kwargs["pets_slug"]
            }
        )


# def edit_page(request, username, pets_slug):
#     pet = Pet.objects.get(slug=pets_slug)
#
#     form = PetEditForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("details-page", username="username", pets_slug=pet.slug)
#
#     context = {
#         "pet": pet,
#         "form": form
#     }

    # return render(request, "pets/pet-edit-page.html", context)
