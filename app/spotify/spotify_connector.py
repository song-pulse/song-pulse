import tekore as tk
from sqlalchemy.orm import Session

from app import crud
from app.schemas.song import SongCreate


def queue_song(db: Session, song_url: str, spotify_username: str):
    if spotify_username:
        conf = tk.config_from_environment()
        cred = tk.Credentials(*conf)
        spotify = tk.Spotify()
        spotify_data = crud.spotify.get(db_session=db, id=spotify_username)
        token = cred.refresh_user_token(spotify_data.refresh_token)
        with spotify.token_as(token):
            uri = "spotify:track:" + song_url.split("/").pop(-1)
            spotify.playback_queue_add(uri)
    else:
        print("ERROR: NO USERNAME - " + str(spotify_username))


def get_left_playtime(db: Session, spotify_username: str) -> int:
    if spotify_username:
        conf = tk.config_from_environment()
        cred = tk.Credentials(*conf)
        spotify = tk.Spotify()
        spotify_data = crud.spotify.get(db_session=db, id=spotify_username)
        token = cred.refresh_user_token(spotify_data.refresh_token)
        with spotify.token_as(token):
            current = spotify.playback_currently_playing()
            if current:
                return current.item.duration_ms - current.progress_ms
            else:
                return 0
    else:
        return 0


def add_songs_for_playlist(db, playlist_id: int, playlist_link: str):
    client_id, client_secret, redirect_uri = tk.config_from_environment()
    token = tk.request_client_token(client_id, client_secret)
    spotify = tk.Spotify(token)

    playlist = spotify.playlist(
        playlist_id=playlist_link.split("/").pop(-1).split("?").pop(0))  # ask spotify for tracks
    for item in playlist.tracks.items:
        if item.track:
            name = item.track.name + " - " + item.track.artists.pop().name
            link = item.track.href
            duration = item.track.duration_ms
            crud.song.create_with_playlist(db, obj_in=SongCreate(name=name, link=link, duration=duration),
                                           playlist_id=playlist_id)
