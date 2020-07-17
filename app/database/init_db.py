from app import crud
from app.schemas.participant import ParticipantCreate
from app.schemas.playlist import PlaylistCreate
from app.schemas.sensor import SensorCreate
from app.schemas.setting import SettingCreate
from app.schemas.song import SongCreate


# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.util.spotify_connector import add_songs_for_playlist


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    participants = crud.participant.get_multi(db_session)
    if len(participants) < 1:
        participant_in = ParticipantCreate(name="P1")
        playlist_in = PlaylistCreate(type="Relax",
                                     link="https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=ImmxuERbS4C8UAyQfYUDqw")
        playlist2_in = PlaylistCreate(type="Motivate",
                                      link="https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy?si=6AtOTL6VR5ipCTI2zD3Rzg")
        playlist3_in = PlaylistCreate(type="Balance",
                                      link="https://open.spotify.com/playlist/0011i6xvtbolmkbqVut6Y5?si=pjgea7sjT6OVENHLx_q2LA")

        sensor_in = SensorCreate(name="EDA", frequency=10)
        sensor2_in = SensorCreate(name="IBI", frequency=10)
        sensor3_in = SensorCreate(name="TEMP", frequency=10)
        sensor4_in = SensorCreate(name="ACC", frequency=10)

        crud.sensor.create(db_session, obj_in=sensor_in)
        crud.sensor.create(db_session, obj_in=sensor2_in)
        crud.sensor.create(db_session, obj_in=sensor3_in)
        crud.sensor.create(db_session, obj_in=sensor4_in)

        crud.participant.create(db_session, obj_in=participant_in)
        crud.playlist.create_with_participant(db_session, obj_in=playlist_in, participant_id=1)
        add_songs_for_playlist(db=db_session, playlist_id=1, playlist_link=playlist_in.link)
        crud.playlist.create_with_participant(db_session, obj_in=playlist2_in, participant_id=1)
        add_songs_for_playlist(db=db_session, playlist_id=2, playlist_link=playlist2_in.link)
        crud.playlist.create_with_participant(db_session, obj_in=playlist3_in, participant_id=1)
        add_songs_for_playlist(db=db_session, playlist_id=3, playlist_link=playlist3_in.link)

    setting = crud.setting.get(db_session)
    if not setting:
        setting = SettingCreate(stress_threshold=0.1, acc_threshold=18, eda_threshold=3, ibi_threshold=2,
                                prr_threshold=3, temp_baseline=0.3, temp_latency=3, duration=3)
        crud.setting.create(db_session, setting)
