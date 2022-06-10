from django.urls import path
from django.test import SimpleTestCase, override_settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="title"),
    path("/search", views.search, name="search"),
    path("/create", views.createPage, name="create"),
    path("<str:title>/edit", views.editPage, name="edit"),
    path("/random", views.randomizePage, name="random")
]
