from app import crud
from app.schemas.recording import RecordingCreate
from app.schemas.result import ResultCreate
from app.schemas.run import RunCreate
from app.schemas.value import ValueCreate


# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    recording = crud.recording.get(db_session, 1)
    if not recording:
        recording_in = RecordingCreate(total_time=20050)
        recording2_in = RecordingCreate(total_time=3730)
        value_in = ValueCreate(type=55, value=33.3, timestamp=16940)
        value_in2 = ValueCreate(type=54, value=99.2, timestamp=16940)
        value_in3 = ValueCreate(type=55, value=30.1, timestamp=16965)
        value_in4 = ValueCreate(type=55, value=70.9, timestamp=150)
        run_in = RunCreate(is_running=True, current_time=17830)
        run2_in = RunCreate()
        result_in = ResultCreate(song="TEST - SONG", verdict=3, timestamp=16940)
        result2_in = ResultCreate(song="TEST2 - ANOTHER SONG", verdict=1, timestamp=140)

        crud.recording.create_with_participant(db_session, obj_in=recording_in, participant_id=98)
        crud.value.create_with_recording(db_session, obj_in=value_in, recording_id=1)
        crud.value.create_with_recording(db_session, obj_in=value_in2, recording_id=1)
        crud.value.create_with_recording(db_session, obj_in=value_in3, recording_id=1)
        crud.run.create_with_recoding(db_session, obj_in=run_in, recording_id=1)
        crud.result.create_with_run(db_session, obj_in=result_in, run_id=1)

        crud.recording.create_with_participant(db_session, obj_in=recording2_in, participant_id=78)
        crud.value.create_with_recording(db_session, obj_in=value_in4, recording_id=2)
        crud.run.create_with_recoding(db_session, obj_in=run2_in, recording_id=2)
        crud.result.create_with_run(db_session, obj_in=result2_in, run_id=2)
