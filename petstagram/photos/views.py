from django.shortcuts import render

from petstagram.common.models import Like
from petstagram.photos.models import Photo


def add_page(request):

    return render(request, "photos/photo-add-page.html")


def details_page(request, pk):
    photo = Photo.objects.get(id=pk)
    likes = photo.like_set.all()
    comments = photo.photos.all()

    context = {
        "photo": photo,
        "likes": likes,
        "comments": comments
    }

    return render(request, "photos/photo-details-page.html", context)


def edit_page(request, pk):

    return render(request, "photos/photo-edit-page.html")