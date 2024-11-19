from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.common.models import Like
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm
from petstagram.photos.models import Photo

@login_required
def add_page(request):

    form = PhotoCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            photo = form.save(commit=False)

            photo.user = request.user

            photo.save()

            return redirect("home-page")

    context = {
        "form": form
    }

    return render(request, "photos/photo-add-page.html", context)


@login_required
def details_page(request, pk):
    photo = Photo.objects.get(id=pk)
    likes = photo.like_set.all()
    comments = photo.photos.all()
    comment_form = CommentForm

    photo.has_liked = photo.like_set.filter(user=request.user).exists()
    context = {
        "photo": photo,
        "likes": likes,
        "comments": comments,
        "comment_form": comment_form
    }

    return render(request, "photos/photo-details-page.html", context)

@login_required
def edit_page(request, pk):

    photo = Photo.objects.get(id=pk)

    form = PhotoEditForm(request.POST or None, instance=photo)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("ph-details-page", pk=photo.id)

    context = {
        "form": form,
        "photo": photo
    }

    return render(request, "photos/photo-edit-page.html", context)


@login_required
def delete_page(request, pk):
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return redirect("home-page")