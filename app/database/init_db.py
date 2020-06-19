from app import crud
from app.schemas.participant import ParticipantCreate
from app.schemas.playlist import PlaylistCreate
from app.schemas.sensor import SensorCreate
from app.schemas.setting import SettingCreate
from app.schemas.song import SongCreate


# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


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
                                      link="https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy?si=6AtOTL6VR5ipCTI2zD3Rzg")
        song_in = SongCreate(name="Olalla",
                             link="https://api.spotify.com/v1/tracks/4d4OJTq2Yl7TyiuGMLxa1h")
        song2_in = SongCreate(name="Na Na Na",
                              link="https://api.spotify.com/v1/tracks/4wEleZDYnwkHHudmxR23omA")
        song3_in = SongCreate(name="Don't Let Me Down",
                              link="https://api.spotify.com/v1/tracks/36fHADliwp4ColP0Gypg5W")

        sensor_in = SensorCreate(name="EDA", frequency=180)
        sensor2_in = SensorCreate(name="IBI", frequency=180)
        sensor3_in = SensorCreate(name="TEMP", frequency=60)
        sensor4_in = SensorCreate(name="ACC", frequency=180)

        crud.sensor.create(db_session, obj_in=sensor_in)
        crud.sensor.create(db_session, obj_in=sensor2_in)
        crud.sensor.create(db_session, obj_in=sensor3_in)
        crud.sensor.create(db_session, obj_in=sensor4_in)

        crud.participant.create(db_session, obj_in=participant_in)
        crud.playlist.create_with_participant(db_session, obj_in=playlist_in, participant_id=1)
        crud.song.create_with_playlist(db_session, obj_in=song_in, playlist_id=1)
        crud.playlist.create_with_participant(db_session, obj_in=playlist2_in, participant_id=1)
        crud.song.create_with_playlist(db_session, obj_in=song2_in, playlist_id=2)
        crud.playlist.create_with_participant(db_session, obj_in=playlist3_in, participant_id=1)
        crud.song.create_with_playlist(db_session, obj_in=song3_in, playlist_id=3)

    setting = crud.setting.get(db_session)
    if not setting:
        setting = SettingCreate(stress_threshold=0.1, acc_threshold=0.5, eda_threshold=0.01, ibi_threshold=2,
                                prr_threshold=3, temp_baseline=0.3, temp_latency=3, duration=3)
        crud.setting.create(db_session, setting)
