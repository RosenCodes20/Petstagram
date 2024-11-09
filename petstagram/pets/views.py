from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


class AddPetPage(CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = "pets/pet-add-page.html"
    success_url = reverse_lazy("profile-details", kwargs={"pk": 1})

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


def delete_page(request, username, pets_slug):

    pet = Pet.objects.get(slug=pets_slug)

    form = PetDeleteForm(request.POST or None, instance=pet)

    if request.method == "POST":
        if form.is_valid():
            pet.delete()
            return redirect("profile-details", pk=1)

    context = {
        "pet": pet,
        "form": form
    }

    return render(request, "pets/pet-delete-page.html", context)


class PetDetailsPage(DetailView):
    model = Pet
    template_name = "pets/pet-details-page.html"
    context_object_name = "pet"
    slug_url_kwarg = "pets_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["photos"] = self.object.tagged_pets.all()
        context["comments"] = CommentForm

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


class EditPetPage(UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = "pets/pet-edit-page.html"
    slug_url_kwarg = "pets_slug"
    context_object_name = "pet"

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
