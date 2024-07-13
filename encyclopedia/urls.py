from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:topic>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new")
]
