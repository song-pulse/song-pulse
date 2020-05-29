from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks, status, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.preprocessing.stream import Stream
from app.schemas.file import File, FileCreate
from app.schemas.participant import Participant, ParticipantCreate
from app.schemas.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from app.schemas.recording import Recording, RecordingCreate
from app.schemas.result import Result, ResultUpdate
from app.schemas.run import Run, RunCreate
from app.schemas.value import Value, ValueCreate
from app.api import deps

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
async def create_value(*, part_id: int, rec_id: int, file_id: int, value: ValueCreate, db: Session = Depends(deps.get_db)):
    fresh_value = crud.value.create_with_file(db_session=db, obj_in=value, file_id=file_id)
    return fresh_value


@router.get("/{part_id}/recordings/{rec_id}/runs", response_model=List[Run])
async def get_runs(*, rec_id: int, db: Session = Depends(deps.get_db)):
    runs = crud.run.get_all_for_recording(db_session=db, recording_id=rec_id)
    return runs


@router.post("/{part_id}/recordings/{rec_id}/runs", response_model=Run)
async def start_run(*, rec_id: int, run: RunCreate, db: Session = Depends(deps.get_db), background_tasks: BackgroundTasks):
    run.is_running = True
    fresh_run = crud.run.create_with_recoding(db_session=db, obj_in=run, recording_id=rec_id)
    background_tasks.add_task(Stream.start, fresh_run, db)
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