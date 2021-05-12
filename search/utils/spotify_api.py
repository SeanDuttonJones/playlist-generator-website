"""
    Author: Sean Dutton-Jones
    Date: April 30, 2020
    Description: Implements some functions to access the Spotify API. 
"""

import requests
import base64
import time
import json

class SpotifyAPI():

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = ""
        self._last_checked = 0 # last time the access token was renewed

    # Base64 encoding of a message. Code from: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/#encodingstringswithpython
    def _base64_encode(self, message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    # Authorization
    def _get_access_token(self):
        current_time = time.time()
        if(current_time - self._last_checked >= 3600):
            authorization_text = self._base64_encode(self.client_id + ':' + self.client_secret)
            access_data = requests.post("https://accounts.spotify.com/api/token", 
                data = {"grant_type": "client_credentials"}, 
                headers = {"Authorization": "Basic " + authorization_text})

            self._last_checked = current_time;
            self._access_token = access_data.json()["access_token"]

        return self._access_token

    # Get a track
    def get_track(self, track_id):
        track = requests.get("https://api.spotify.com/v1/tracks/" + track_id,
                headers = {"Authorization": "Bearer " + self._get_access_token()})

        return track.json()

    # Get tracks from a specified album
    def get_albums_tracks(self, album_id):
        tracks = requests.get("https://api.spotify.com/v1/albums/" + album_id + "/tracks",
            headers = {"Authorization": "Bearer " + self._get_access_token()})

        return tracks.json()["items"]

    # Get tracks from a playlist
    def get_playlist_tracks(self, playlist_id):
        tracks = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks",
            headers = {"Authorization": "Bearer " + self._get_access_token()})

        return tracks.json()["items"]

    # Get audio features for several tracks
    def get_features_for_tracks(self, track_ids):
        audio_features = requests.get("https://api.spotify.com/v1/audio-features/",
            params = {"ids": ','.join(track_ids)},
            headers = {"Authorization": "Bearer " + self._get_access_token()})

        return audio_features.json()["audio_features"]

    # Get audio analysis for a track
    def get_audio_analysis_for_track(self, track_id):
        audio_analysis = requests.get("https://api.spotify.com/v1/audio-analysis/" + track_id,
            headers={"Authorization": "Bearer " + self._get_access_token()})

        return audio_analysis.json()

    # Gets songs which are similar to the seed track
    def get_recommendations(self, track_id):
        recommendations = requests.get("https://api.spotify.com/v1/recommendations",
            params={"seed_tracks": track_id},
            headers={"Authorization": "Bearer " + self._get_access_token()})

        return recommendations.json()["tracks"]

    # search spotify for a song
    def search(self, query):
        search = requests.get("https://api.spotify.com/v1/search",
            params={"q": query, "type": "track", "limit": 5},
            headers={"Authorization": "Bearer " + self._get_access_token()})

        return search.json()

    # create an empty playlist
    def create_playlist(self, name, user_id, access_token):
        playlist = requests.post("https://api.spotify.com/v1/users/" + user_id + "/playlists",
            data=json.dumps({"name": name, "public": False}),
            headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"})

        return playlist.json()

    # add tracks to a playlist
    def add_tracks_to_playlist(self, playlist_id, track_ids, access_token):
        playlist = requests.post("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks",
            data=json.dumps({"uris": track_ids}),
            headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"})

        return playlist.json()

    def get_user_profile(self, access_token):
        me = requests.get("https://api.spotify.com/v1/me",
            headers={"Authorization": "Bearer " + access_token})

        return me.json()