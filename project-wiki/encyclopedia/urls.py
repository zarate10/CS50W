from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("create/wiki", views.create, name="create")
]
