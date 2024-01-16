from django.urls import path

from . import views

urlpatterns = [
    path("", views.create_tour_view, name="create_tour"),
    path(
        "theme_suggestions/",
        views.theme_suggestions_view,
        name="theme_suggestions",
    ),
]
