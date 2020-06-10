import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app import crud
from app.schemas.song import SongCreate

cred_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=cred_manager)


def add_songs_for_playlist(db, playlist_id: int, playlist_link: str):
    tracks = sp.playlist_tracks(playlist_id=playlist_link.split("/").pop(-1).split("?").pop(0),
                                fields="items(track(name,href))")  # ask spotify for tracks
    for item in tracks['items']:
        name = item['track']['name']
        link = item['track']['href']
        crud.song.create_with_playlist(db, obj_in=SongCreate(name=name, link=link), playlist_id=playlist_id)