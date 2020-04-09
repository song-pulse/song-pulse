from app import crud
from app.schemas.participant import ParticipantCreate
from app.schemas.song import SongCreate
from app.schemas.recording import RecordingCreate
from app.schemas.result import ResultCreate
from app.schemas.run import RunCreate
from app.schemas.value import ValueCreate
from app.schemas.sensor import SensorCreate
from app.schemas.playlist import PlaylistCreate


# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    recording = crud.participant.get(db_session, 1)
    if not recording:
        participant_in = ParticipantCreate(name="DIMITRI")
        participant2_in = ParticipantCreate(name="ANJA")
        playlist_in = PlaylistCreate(name="Rap", link="https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=ImmxuERbS4C8UAyQfYUDqw")
        playlist2_in = PlaylistCreate(name="Motivation", link="https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy?si=6AtOTL6VR5ipCTI2zD3Rzg")
        song_in = SongCreate(name="Tyler, the Creator - anderes Lied", link="https://open.spotify.com/track/3jHdKaLCkuNEkWcLVmQPCX?si=W7UHEeb0Rn68ULB5SSwCQw")
        song2_in = SongCreate(name="Hoechste Eisenbahn - Liedlein", link="https://open.spotify.com/track/7qjxi7PZDfXSMCcolbW5yt?si=F_4NW5FwSo2BGxbWk-ndqA")
        recording_in = RecordingCreate(total_time=20050)
        recording2_in = RecordingCreate(total_time=3730)
        sensor_in = SensorCreate(name="EDA")
        sensor2_in = SensorCreate(name="BVP")
        value_in = ValueCreate(sensor_id=2, value=33.3, timestamp=16940)
        value_in2 = ValueCreate(sensor_id=1, value=99.2, timestamp=16940)
        value_in3 = ValueCreate(sensor_id=2, value=30.1, timestamp=16965)
        value_in4 = ValueCreate(sensor_id=2, value=70.9, timestamp=150)
        run_in = RunCreate(is_running=True, current_time=17830)
        run2_in = RunCreate()
        result_in = ResultCreate(song_id=1, verdict=3, timestamp=16940)
        result2_in = ResultCreate(song_id=2, verdict=1, timestamp=140)

        crud.sensor.create(db_session, obj_in=sensor_in)
        crud.sensor.create(db_session, obj_in=sensor2_in)

        crud.participant.create(db_session, obj_in=participant_in)
        crud.playlist.create_with_participant(db_session, obj_in=playlist_in, participant_id=1)
        crud.song.create_with_playlist(db_session, obj_in=song_in, playlist_id=1)
        crud.recording.create_with_participant(db_session, obj_in=recording_in, participant_id=1)
        crud.value.create_with_recording(db_session, obj_in=value_in, recording_id=1)
        crud.value.create_with_recording(db_session, obj_in=value_in2, recording_id=1)
        crud.value.create_with_recording(db_session, obj_in=value_in3, recording_id=1)
        crud.run.create_with_recoding(db_session, obj_in=run_in, recording_id=1)
        crud.result.create_with_run(db_session, obj_in=result_in, run_id=1)

        crud.participant.create(db_session, obj_in=participant2_in)
        crud.playlist.create_with_participant(db_session, obj_in=playlist2_in, participant_id=2)
        crud.song.create_with_playlist(db_session, obj_in=song2_in, playlist_id=2)
        crud.recording.create_with_participant(db_session, obj_in=recording2_in, participant_id=2)
        crud.value.create_with_recording(db_session, obj_in=value_in4, recording_id=2)
        crud.run.create_with_recoding(db_session, obj_in=run2_in, recording_id=2)
        crud.result.create_with_run(db_session, obj_in=result2_in, run_id=2)
