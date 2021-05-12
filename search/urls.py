from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("playlist/", views.playlist, name='playlist'),
    path("playlist/<str:track_id>/", views.playlist, name="playlist"),
    path("validation/", views.validate, name="validate"),
    path("save_playlist/", views.save_playlist, name="save_playlist"),
    path("search_spotify/<str:user_input>/", views.search_spotify, name="search_spotify")
]