from django.shortcuts import render, redirect

from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


def add_page(request):

    form = PetCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("profile-details", pk=1)


    context = {
        "form": form
    }

    return render(request, "pets/pet-add-page.html", context)


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


def details_page(request, username, pets_slug):

    pet = Pet.objects.get(slug=pets_slug)
    photos = Photo.objects.all()

    context = {
        "pet": pet,
        "photos": photos
    }

    return render(request, "pets/pet-details-page.html", context)


def edit_page(request, username, pets_slug):
    pet = Pet.objects.get(slug=pets_slug)

    form = PetEditForm(request.POST or None, instance=pet)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("details-page", username="username", pets_slug=pet.slug)

    context = {
        "pet": pet,
        "form": form
    }

    return render(request, "pets/pet-edit-page.html", context)
