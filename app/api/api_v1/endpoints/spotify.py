import spotipy
from fastapi import APIRouter, Cookie
from starlette.responses import RedirectResponse, Response

router = APIRouter()

auth_manager = spotipy.oauth2.SpotifyOAuth()
auth_manager.scope = "user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=auth_manager)


@router.get("/whoami")
async def show(username: str = Cookie(None)):
    if username:
        auth_manager.username = username
        display_name = spotify.me()["display_name"]
        auth_manager.username = None
        return "ALL DONE, HELLO " + display_name + "!"
    return Response(status_code=400)


@router.get("/callback")
async def callback(code: str):
    auth_manager.username = code
    auth_manager.get_access_token(code, as_dict=False)
    auth_manager.username = None
    response = RedirectResponse("whoami")
    response.set_cookie("username", code)
    return response


@router.get("/authorize")
async def authorize():
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(auth_url)


@router.post("/queue")
async def queue(track: str, username: str = Cookie(None)):
    if username:
        auth_manager.username = username
        spotify.add_to_queue(track)
        auth_manager.username = None
        return Response
    return Response(status_code=400)
