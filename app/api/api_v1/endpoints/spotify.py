import tekore as tk
from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

from app import crud
from app.api import deps
from app.schemas.spotify import SpotifyCreate, SpotifyUpdate

router = APIRouter()

conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()


@router.get("/whoami")
async def show(username: str = Cookie(None), db: Session = Depends(deps.get_db)):
    if username:
        spotify_data = crud.spotify.get(db_session=db, id=username)
        token = cred.refresh_user_token(spotify_data.refresh_token)
        with spotify.token_as(token):
            response = Response()
            response.set_cookie("username", spotify.current_user().id, path="/", httponly=True)
            return response
    return Response(status_code=400)


@router.get("/callback")
async def callback(code: str, db: Session = Depends(deps.get_db)):
    token = cred.request_user_token(code)
    with spotify.token_as(token):
        info = spotify.current_user()
        existing = crud.spotify.get(db_session=db, id=info.id)
        if not existing:
            crud.spotify.create(db_session=db, obj_in=SpotifyCreate(id=info.id, token=token.access_token,
                                                                    refresh_token=token.refresh_token,
                                                                    expires_at=token.expires_at))
        else:
            crud.spotify.update(db_session=db, db_obj=existing, obj_in=SpotifyUpdate(id=info.id,
                                                                                     token=token.access_token,
                                                                                     refresh_token=token.refresh_token,
                                                                                     expires_at=token.expires_at))
    response = RedirectResponse("whoami")
    response.set_cookie("username", info.id, path="/", httponly=True)
    return response


@router.get("/authorize")
async def authorize():
    auth_url = cred.user_authorisation_url(scope=tk.scope.user_modify_playback_state)
    return RedirectResponse(auth_url)
