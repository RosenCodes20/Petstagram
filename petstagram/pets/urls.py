from django.urls import path, include

from petstagram.pets import views

urlpatterns = [
    path("add/", views.AddPetPage.as_view(), name="add-page"),
    path("<str:username>/pet/<slug:pets_slug>/", include([
        path("", views.PetDetailsPage.as_view(), name="details-page"),
        path("edit/", views.EditPetPage.as_view(), name="edit-page"),
        path("delete/", views.delete_page, name="delete-page")
    ])),

]