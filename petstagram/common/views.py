from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchBarForm
from petstagram.common.models import Like, Comment
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


class Index(ListView):
    model = Photo
    template_name = "common/home-page.html"
    paginate_by = 2
    context_object_name = "photos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["comment_form"] = CommentForm

        context["search_bar_form"] = SearchBarForm(self.request.GET)

        context["comments"] = Comment.objects.all()

        for photo in context["photos"]:
            photo.has_liked = photo.like_set.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get("pet_name")

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains=pet_name
            )

        return queryset


# def index(request):
#
#     photos = Photo.objects.all()
#     comment_form = CommentForm()
#     comments = Comment.objects.all()
#     search_bar_form = SearchBarForm(request.GET)
#
#     if search_bar_form.is_valid():
#         cleaned_pet_name = request.GET.get("pet_name")
#
#         if cleaned_pet_name:
#             photos = photos.filter(tagged_pets__name__icontains=cleaned_pet_name)
#
#     context = {
#         "photos": photos,
#         "comment_form": comment_form,
#         "comments": comments,
#         "search_form": search_bar_form
#     }
#
#     return render(request, "common/home-page.html", context)


@login_required
def like_functionality(request, pk):

    photo = Photo.objects.get(id=pk)
    liked_obj = Like.objects.filter(to_photo_id=photo.id, user=request.user).first()


    if liked_obj:
        liked_obj.delete()

    else:
        like = Like(to_photo_id=photo.id, user=request.user)
        like.save()

    return redirect(request.META["HTTP_REFERER"] + f"#{photo.id}")


def share_functionality(request, pk):
    photo = Photo.objects.get(id=pk)
    copy(request.META["HTTP_REFERER"] + resolve_url("ph-details-page", photo.id))

    return redirect(request.META["HTTP_REFERER"] + f"#{photo.id}")

@login_required
def comment_functionality(request, pk):

    if request.method == "POST":

        comment_form = CommentForm(request.POST)
        photo = Photo.objects.get(id=pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            return redirect(request.META.get("HTTP_REFERER") + f"#{photo}")