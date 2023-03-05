from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="entryPage"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/newpage/", views.newPage, name="newPage"),
    path("wiki/editpage/<str:title>", views.editPage, name="editPage"),
    path("randomPage", views.randomPage, name="randomPage")
]
