from app import crud
from app.schemas.participant import ParticipantCreate
from app.schemas.setting import SettingCreate
from app.schemas.song import SongCreate
from app.schemas.recording import RecordingCreate
from app.schemas.result import ResultCreate
from app.schemas.run import RunCreate
from app.schemas.value import ValueCreate
from app.schemas.file import FileCreate
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
        playlist_in = PlaylistCreate(type="Relax",
                                     link="https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=ImmxuERbS4C8UAyQfYUDqw")
        playlist2_in = PlaylistCreate(type="Motivate",
                                      link="https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy?si=6AtOTL6VR5ipCTI2zD3Rzg")
        song_in = SongCreate(name="Tyler, the Creator - anderes Lied",
                             link="https://open.spotify.com/track/3jHdKaLCkuNEkWcLVmQPCX?si=W7UHEeb0Rn68ULB5SSwCQw")
        song2_in = SongCreate(name="Hoechste Eisenbahn - Liedlein",
                              link="https://open.spotify.com/track/7qjxi7PZDfXSMCcolbW5yt?si=F_4NW5FwSo2BGxbWk-ndqA")
        recording_in = RecordingCreate(name="Test")
        recording2_in = RecordingCreate(name="Early Morning")
        file_in = FileCreate(sensor_id=2, name="file1.csv")
        file2_in = FileCreate(sensor_id=1, name="file2.csv")
        file3_in = FileCreate(sensor_id=2, name="file3.csv")
        value_in = ValueCreate(file_id=1, value1=11.1, value2=11.1, value3=11.1, timestamp=16940)
        value_in2 = ValueCreate(file_id=2, value1=99.2, value2=11.1, value3=11.1, timestamp=16940)
        value_in3 = ValueCreate(file_id=1, value1=11.5, value2=22.6, value3=33.7, timestamp=16965)
        value_in4 = ValueCreate(file_id=3, value1=70.9, value2=0.0, value3=0.0, timestamp=150)
        run_in = RunCreate(is_running=True, current_time=17830)
        run2_in = RunCreate()
        result_in = ResultCreate(song_id=1, verdict=3, timestamp=16940, input="test")
        result2_in = ResultCreate(song_id=2, verdict=1, timestamp=140, input="value EDA changed to 1")

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
        crud.recording.create_with_participant(db_session, obj_in=recording_in, participant_id=1)
        crud.file.create_with_recording(db_session, obj_in=file_in, recording_id=1)
        crud.file.create_with_recording(db_session, obj_in=file2_in, recording_id=1)
        crud.value.create_with_file(db_session, obj_in=value_in, file_id=1)
        crud.value.create_with_file(db_session, obj_in=value_in2, file_id=2)
        crud.value.create_with_file(db_session, obj_in=value_in3, file_id=1)
        crud.run.create_with_recoding(db_session, obj_in=run_in, recording_id=1)
        crud.result.create_with_run(db_session, obj_in=result_in, run_id=1)

        crud.participant.create(db_session, obj_in=participant2_in)
        crud.playlist.create_with_participant(db_session, obj_in=playlist2_in, participant_id=2)
        crud.song.create_with_playlist(db_session, obj_in=song2_in, playlist_id=2)
        crud.recording.create_with_participant(db_session, obj_in=recording2_in, participant_id=2)
        crud.file.create_with_recording(db_session, obj_in=file3_in, recording_id=2)
        crud.value.create_with_file(db_session, obj_in=value_in4, file_id=3)
        crud.run.create_with_recoding(db_session, obj_in=run2_in, recording_id=2)
        crud.result.create_with_run(db_session, obj_in=result2_in, run_id=2)

    setting = crud.setting.get(db_session, id=1)
    if not setting:
        setting = SettingCreate(stress_threshold=0.1, acc_threshold=0.5, eda_threshold=0.01, ibi_threshold=2,
                                prr_threshold=3, temp_baseline=0.3, temp_latency=3, duration=3)
        crud.setting.create(db_session, setting)
