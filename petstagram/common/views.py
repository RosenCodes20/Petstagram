from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.models import Like
from petstagram.photos.models import Photo


def index(request):

    photos = Photo.objects.all()

    context = {
        "photos": photos
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