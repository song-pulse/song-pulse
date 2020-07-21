from datetime import datetime, timedelta

from numpy import random
from sqlalchemy.orm import Session

from app import crud
from app.models.song import Song
from app.preprocessing.data_for_time import DataForTime
from app.schemas.result import ResultCreate
from app.spotify.spotify_connector import get_left_playtime, queue_song


def queue(db_session: Session, data: DataForTime, action: int, part_id: int, spotify_username: str) -> ResultCreate:
    song = get_song_for_action(db_session=db_session, action=action, participant_id=part_id)
    link = song.link
    duration = song.duration
    queue_song(db=db_session, song_url=link, spotify_username=spotify_username)
    wait_for_ms = get_left_playtime(db_session, spotify_username) + duration
    song_plays_until = datetime.now() + timedelta(milliseconds=wait_for_ms)

    return ResultCreate(timestamp=data.timestamp, song_id=song.id, verdict=-1, input=str(data), action=action,
                        song_queued=True, song_plays_until=song_plays_until)


def get_song_for_action(db_session: Session, action: int, participant_id: int) -> Song:
    pl_type = ''
    if action == 0:
        pl_type = 'Motivate'
        # choose  motivating playlist
    elif action == 1:
        pl_type = 'Balance'
        # choose  normal playlist
    elif action == 2:
        pl_type = 'Relax'
        # choose  relaxing playlist
    playlist = crud.playlist.get_by_participant_and_type(db_session=db_session, participant_id=participant_id,
                                                         plist_type=pl_type)
    random_song = random.randint(len(playlist.songs)-1)
    return playlist.songs[random_song]


def is_queue_finished(db_session: Session, run_id: int) -> bool:
    last_queued_result = crud.result.get_last_queued(db_session, run_id)
    # only if the last song we queued is about to end!
    return (not last_queued_result) or datetime.now() + timedelta(seconds=20) >= last_queued_result.song_plays_until
