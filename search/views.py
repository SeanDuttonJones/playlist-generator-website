from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from search.utils.spotify_api import SpotifyAPI
import json

# Create your views here.
def index(request):
    return render(request, "index.html")

@ensure_csrf_cookie
def playlist(request, track_id):
    spotify = SpotifyAPI("xxx", "xxx")

    seed_track = spotify.get_track(track_id)

    tracks = spotify.get_recommendations(track_id)
    for track in tracks:
        artist_names = []
        for artist in track["artists"]:
            artist_names.append(artist["name"])

        track.update({"artists_names": ", ".join(artist_names)})

    context = {
        "seed_track_id": track_id,
        "seed_track_title": seed_track["name"],
        "seed_artist": seed_track["artists"][0]["name"],
        "seed_cover_pic": seed_track["album"]["images"][0]["url"],
        "tracks": tracks
    }
    return render(request, "playlist.html", context=context)

def search_spotify(request, user_input):
    spotify = SpotifyAPI("xxx", "xxx")

    search_results = spotify.search(user_input)

    tracks = []
    for item in search_results["tracks"]["items"]:
        artist_names = []
        for artist in item["artists"]:
            artist_names.append(artist["name"])

        tracks.append({"id": item["id"], "track": item["name"], "artists": artist_names})

    return HttpResponse(content=json.dumps(tracks))

def validate(request):
    return render(request, "validate.html")

def save_playlist(request):
    spotify = SpotifyAPI("xxx", "xxx")

    playlist_name = request.POST.get("playlist_name")
    access_token = request.POST.get("access_token")

    track_ids = request.POST.getlist("track_ids[]")
    for i in range(0, len(track_ids)):
        track_ids[i] = "spotify:track:" + track_ids[i]

    user_profile = spotify.get_user_profile(access_token)
    
    playlist_empty = spotify.create_playlist(playlist_name, user_profile["id"], access_token)
    playlist_full = spotify.add_tracks_to_playlist(playlist_empty["id"], track_ids, access_token)
    return HttpResponse(content="")