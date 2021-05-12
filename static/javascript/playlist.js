$(document).ready(function() {
    seed_track_id = $("#seed-track-header").attr("seed_track_id");

    if(sessionStorage.getItem(seed_track_id) === null) {
        // Create new storage
        tracks_names = $(".track-name");
        track_ids = $(".track");
        artists_names = $(".artist-names");
        album_cover_pics = $(".album-cover-pic");
        explicit_badges = $(".badge-explicit");
        //11zf7m4vw9Ze7cer9Nyhk1
        var playlist_items = [];

        for(var i = 0; i < tracks_names.length; i++) {
            playlist_items.push({
                "track_name": $(tracks_names[i]).text(),
                "track_id": $(track_ids[i]).attr("track_id"),
                "artists_names": $(artists_names[i]).text(),
                "album_cover_pic": $(album_cover_pics[i]).attr("src"),
                "explicit": !$(explicit_badges[i]).hasClass("d-none")
            });
        }

        sessionStorage.setItem(seed_track_id, JSON.stringify(playlist_items));
    } else {
        // Load saved storage
        var playlist_items = JSON.parse(sessionStorage.getItem(seed_track_id));

        tracks_names = $(".track-name");
        track_ids = $(".track");
        artists_names = $(".artist-names");
        album_cover_pics = $(".album-cover-pic");
        explicit_badges = $(".badge-explicit");

        for(var i = 0; i < tracks_names.length; i++) {
            $(tracks_names[i]).text(playlist_items[i]["track_name"]);
            $(track_ids[i]).attr("track_id", playlist_items[i]["track_id"]);
            $(artists_names[i]).text(playlist_items[i]["artists_names"]);
            $(album_cover_pics[i]).attr("src", playlist_items[i]["album_cover_pic"]);
            $(explicit_badges[i]).toggleClass("d-none", !playlist_items[i]["explicit"]);
        }
    }

    function getPlaylistName() {
        var name = $("#playlist-title").val();
        if(name) {
            return name;
        }

        return null;
    }

    $("#spotify-connect").on("click", function(e) {
        playlist_name = getPlaylistName();
        if(playlist_name !== null) {
            url = "https://accounts.spotify.com/authorize" +
            "?client_id=f74f5f934a294935b04b2f2de0fb1821" +
            "&response_type=token" +
            "&scope=playlist-modify-private" +
            "&redirect_uri=http://127.0.0.1:8000/search/validation/";

            window.open(url);
            $(window).focus(function() {
                var access_token = localStorage.getItem("access_token"); // If the user fails to validate, access_token will have value "error"
                saveUserPlaylist(access_token);
                $(this).off();
            });
        } else {
            alert("Please name your playlist before saving to Spotify.");
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getTrackIDs() {
        tracks = $(".track");
        track_ids = [];

        for(var i = 0; i < tracks.length; i++) {
            track_ids.push($(tracks[i]).attr("track_id"));
        }

        return track_ids;
    }

    function saveUserPlaylist(access_token) {
        var csrftoken = getCookie("csrftoken");
        var track_ids = getTrackIDs();
        var playlist_name = getPlaylistName();

        $.ajax({
            type: "POST",
            url: "../../save_playlist/",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: {
                "playlist_name": playlist_name,
                "access_token": access_token,
                "track_ids": track_ids
            },
            success: function(result) {}
        });
    }
});