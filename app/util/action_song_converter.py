from app import crud


def get_song_from_spotify(db_session, action, participant_id):
    pl_type = ''
    if action == 0:
        pl_type = 'Motivate'
        # choose  motivating playlist
    elif action == 1:
        # TODO: here should be a third playlisttype added -> for example normal
        pl_type = 'Balance'
        # choose  normal playlist
    elif action == 2:
        pl_type = 'Relax'
        # choose  relaxing playlist
    playlist = crud.playlist.get_by_participant_and_type(db_session=db_session, participant_id=participant_id,
                                                         plist_type=pl_type)
    return playlist.songs[0].id
