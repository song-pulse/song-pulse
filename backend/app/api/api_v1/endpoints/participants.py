from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.app import crud
from backend.app.core import celery_app
from backend.app.schemas.file import File, FileCreate
from backend.app.schemas.participant import Participant, ParticipantCreate
from backend.app.schemas.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from backend.app import Recording, RecordingCreate
from backend.app import Result, ResultUpdate
from backend.app import Run, RunCreate
from backend.app.schemas.value import Value, ValueCreate
from backend.app.schemas.timestamp_values import TimestampValues
from backend.app.api import deps

router = APIRouter()


@router.get("/", response_model=List[Participant])
async def read_participants(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    recordings = crud.participant.get_multi(db, skip=skip, limit=limit)
    return recordings


@router.post("/", response_model=Participant)
async def create_participant(*, participant: ParticipantCreate, db: Session = Depends(deps.get_db)):
    fresh_participant = crud.participant.create(db, participant)
    return fresh_participant


@router.get("/{part_id}", response_model=Participant)
async def read_participant(part_id: int, db: Session = Depends(deps.get_db)):
    recordings = crud.participant.get(db, part_id)
    return recordings


@router.delete("/{part_id}", status_code=status.HTTP_200_OK)
async def delete_participant(*, part_id: int, db: Session = Depends(deps.get_db)):
    crud.participant.remove(db_session=db, id=part_id)


@router.get("/{part_id}/recordings", response_model=List[Recording])
async def read_recordings(part_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    recordings = crud.recording.get_by_participant(db, participant_id=part_id, skip=skip, limit=limit)
    return recordings


@router.post("/{part_id}/recordings", response_model=Recording)
async def create_recording(*, part_id: int, recording: RecordingCreate, db: Session = Depends(deps.get_db)):
    fresh_recording = crud.recording.create_with_participant(db_session=db, obj_in=recording, participant_id=part_id)
    return fresh_recording


@router.get("/{part_id}/recordings/{rec_id}", response_model=Recording)
async def read_recording(rec_id: int, db: Session = Depends(deps.get_db)):
    recordings = crud.recording.get(db, rec_id)  # TODO perhaps check if rec_id and part_id match
    return recordings


@router.delete("/{part_id}/recordings/{rec_id}", status_code=status.HTTP_200_OK)
async def delete_recording(*, rec_id: int, db: Session = Depends(deps.get_db)):
    crud.recording.remove(db_session=db, id=rec_id)  # TODO perhaps check if rec_id and part_id match


@router.get("/{part_id}/recordings/{rec_id}/files", response_model=List[File])
async def get_files(part_id: int, rec_id: int, db: Session = Depends(deps.get_db)):
    fresh_files = crud.file.get_multi_for_recording(db_session=db, recording_id=rec_id)
    return fresh_files


@router.post("/{part_id}/recordings/{rec_id}/files", response_model=File)
async def create_file(*, part_id: int, rec_id: int, file: FileCreate, db: Session = Depends(deps.get_db)):
    fresh_file = crud.file.create_with_recording(db_session=db, obj_in=file, recording_id=rec_id)
    return fresh_file


@router.delete("/{part_id}/recordings/{rec_id}/files/{file_id}", status_code=status.HTTP_200_OK)
async def delete_file(*, part_id: int, rec_id: int, file_id: int, db: Session = Depends(deps.get_db)):
    crud.file.remove(db_session=db, id=file_id)


@router.get("/{part_id}/recordings/{rec_id}/files/{file_id}/values", response_model=List[Value])
async def get_values(part_id: int, rec_id: int, file_id: int, db: Session = Depends(deps.get_db)):
    fresh_value = crud.value.get_all_for_file(db_session=db, file_id=file_id)
    return fresh_value


@router.post("/{part_id}/recordings/{rec_id}/files/{file_id}/values", response_model=Value)
async def create_value(*, part_id: int, rec_id: int, file_id: int, value: ValueCreate,
                       db: Session = Depends(deps.get_db)):
    fresh_value = crud.value.create_with_file(db_session=db, obj_in=value, file_id=file_id)
    return fresh_value


@router.get("/{part_id}/recordings/{rec_id}/runs", response_model=List[Run])
async def get_runs(*, rec_id: int, db: Session = Depends(deps.get_db)):
    runs = crud.run.get_all_for_recording(db_session=db, recording_id=rec_id)
    return runs


@router.post("/{part_id}/recordings/{rec_id}/runs", response_model=Run)
async def start_run(*, part_id: int, rec_id: int, run: RunCreate, db: Session = Depends(deps.get_db)):
    run.is_running = True
    fresh_run = crud.run.create_with_recoding(db_session=db, obj_in=run, recording_id=rec_id)
    celery_app.send_task("app.worker.run", args=[part_id, rec_id, fresh_run.id, -100, 0, 0, 0, 0, 0, 0])
    return fresh_run


@router.get("/{part_id}/recordings/{rec_id}/runs/{run_id}", response_model=Run)
async def get_run(*, run_id: int, db: Session = Depends(deps.get_db)):
    run = crud.run.get(db_session=db, id=run_id)
    return run


@router.put("/{part_id}/recordings/{rec_id}/runs/{run_id}/results/{result_id}", response_model=Result)
async def update_result(*, result_id: int, result: ResultUpdate, db: Session = Depends(deps.get_db)):
    existing_result = crud.result.get(db_session=db, id=result_id)
    if not existing_result:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_result = crud.result.update(db_session=db, db_obj=existing_result, obj_in=result)
    return updated_result


@router.get("/{part_id}/playlists", response_model=List[Playlist])
async def read_playlists(part_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    playlists = crud.playlist.get_by_participant(db, participant_id=part_id, skip=skip, limit=limit)
    return playlists


@router.post("/{part_id}/playlists", response_model=Playlist)
async def create_playlist(*, part_id: int, playlist: PlaylistCreate, db: Session = Depends(deps.get_db)):
    fresh_playlist = crud.playlist.create_with_participant(db, participant_id=part_id, obj_in=playlist)
    return fresh_playlist


@router.put("/{part_id}/playlists", response_model=Playlist)
async def update_playlist(*, part_id: int, playlist: PlaylistUpdate, db: Session = Depends(deps.get_db)):
    existing_playlist = crud.playlist.get_by_participant_and_type(db, part_id, playlist.type)
    if not existing_playlist:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_playlist = crud.playlist.update(db, db_obj=existing_playlist, obj_in=playlist)
    return updated_playlist


# Starts a Recording session including a run!
@router.post("/{part_id}/recordings/start", response_model=Run)
def start_mobile_recording(*, part_id: int, db: Session = Depends(deps.get_db)):
    recording = RecordingCreate(name=str(datetime.now()))
    fresh_recording = crud.recording.create_with_participant(db_session=db, obj_in=recording, participant_id=part_id)
    sensors = crud.sensor.get_multi(db_session=db)
    for sensor in sensors:
        file = FileCreate(sensor_id=sensor.id, name=sensor.name)
        crud.file.create_with_recording(db_session=db, obj_in=file, recording_id=fresh_recording.id)
    run = RunCreate(is_running=True)
    fresh_run = crud.run.create_with_recoding(db_session=db, obj_in=run, recording_id=fresh_recording.id)
    return fresh_run


# Adds timestamp values to an existing recording / run, recording and run are in this case always a 1:1 connection.
# So we don't need to specify a run_id, it's simply always the latest. This assumes that no one manually creates a run
# during a recording session.
# We do not save null values.
@router.post("/{part_id}/recordings/{rec_id}/values/timestamps", response_model=Run)
def create_mobile_value(*, part_id: int, rec_id: int, tv: TimestampValues, db: Session = Depends(deps.get_db)):
    files = crud.file.get_multi_for_recording(db_session=db, recording_id=rec_id)
    for file in files:
        value = None
        if "ibi" in file.name.lower() and tv.ibi is not None:
            value = ValueCreate(timestamp=tv.timestamp, value1=tv.ibi)
        if "eda" in file.name.lower() and tv.eda is not None:
            value = ValueCreate(timestamp=tv.timestamp, value1=tv.eda)
        if "temp" in file.name.lower() and tv.temp is not None:
            value = ValueCreate(timestamp=tv.timestamp, value1=tv.temp)
        if "acc" in file.name.lower() and tv.acc_x is not None:
            value = ValueCreate(timestamp=tv.timestamp, value1=tv.acc_x, value2=tv.acc_y, value3=tv.acc_z)

        if value is not None:
            crud.value.create_with_file(db_session=db, obj_in=value, file_id=file.id)

    current_run = crud.run.get_first_for_recording(db_session=db, recording_id=rec_id)
    celery_app.send_task("app.worker.run", args=[part_id,
                                                 rec_id,
                                                 current_run.id,
                                                 tv.timestamp,
                                                 tv.eda,
                                                 tv.ibi,
                                                 tv.temp,
                                                 tv.acc_x,
                                                 tv.acc_y,
                                                 tv.acc_z])
    return current_run
