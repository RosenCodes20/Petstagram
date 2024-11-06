from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchBarForm
from petstagram.common.models import Like, Comment
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


def index(request):

    photos = Photo.objects.all()
    comment_form = CommentForm()
    comments = Comment.objects.all()
    search_bar_form = SearchBarForm(request.GET)

    if search_bar_form.is_valid():
        cleaned_pet_name = search_bar_form.cleaned_data["pet_name"]
        photos = photos.filter(tagged_pets__name__icontains=cleaned_pet_name)

    context = {
        "photos": photos,
        "comment_form": comment_form,
        "comments": comments,
        "search_form": search_bar_form
    }

    return render(request, "common/home-page.html", context)


def like_functionality(request, pk):

    photo = Photo.objects.get(id=pk)
    liked_obj = Like.objects.filter(to_photo_id=photo.id)

    if liked_obj:
        liked_obj.delete()

    else:
        like = Like(to_photo=photo)
        like.save()

    return redirect(request.META["HTTP_REFERER"] + f"#{photo.id}")


def share_functionality(request, pk):
    photo = Photo.objects.get(id=pk)
    copy(request.META["HTTP_REFERER"] + resolve_url("ph-details-page", photo.id))

    return redirect(request.META["HTTP_REFERER"] + f"#{photo.id}")


def comment_functionality(request, pk):

    if request.method == "POST":

        comment_form = CommentForm(request.POST)
        photo = Photo.objects.get(id=pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.save()
            return redirect(request.META.get("HTTP_REFERER") + f"#{photo}")