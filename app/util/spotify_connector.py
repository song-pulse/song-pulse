import tekore as tk

from app import crud
from app.schemas.song import SongCreate


def queue_song(db, song_url: str, spotify_username: str):
    conf = tk.config_from_environment()
    cred = tk.Credentials(*conf)
    spotify = tk.Spotify()
    spotify_data = crud.spotify.get(db_session=db, id=spotify_username)
    token = cred.refresh_user_token(spotify_data.refresh_token)
    with spotify.token_as(token):
        uri = "spotify:track:" + song_url.split("/").pop(-1)
        print(uri)
        spotify.playback_queue_add(uri)


def add_songs_for_playlist(db, playlist_id: int, playlist_link: str):
    client_id, client_secret, redirect_uri = tk.config_from_environment()
    token = tk.request_client_token(client_id, client_secret)
    spotify = tk.Spotify(token)

    playlist = spotify.playlist(playlist_id=playlist_link.split("/").pop(-1).split("?").pop(0))  # ask spotify for tracks
    for item in playlist.tracks.items:
        name = item.track.name
        link = item.track.href
        crud.song.create_with_playlist(db, obj_in=SongCreate(name=name, link=link), playlist_id=playlist_id)
