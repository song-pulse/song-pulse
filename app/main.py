from typing import List

from fastapi import Depends, BackgroundTasks, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import crud
from app.database.session import Session
from app.schemas.file import File, FileCreate
from app.schemas.participant import Participant, ParticipantCreate
from app.schemas.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from app.schemas.recording import Recording, RecordingCreate
from app.schemas.run import Run, RunCreate
from app.schemas.sensor import Sensor, SensorCreate
from app.schemas.value import Value, ValueCreate

from app.preprocessing.stream import Stream

app = FastAPI()

origins = [
    "https://stream-pulse.herokuapp.com",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


@app.get("/participants", response_model=List[Participant])
async def read_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recordings = crud.participant.get_multi(db, skip=skip, limit=limit)
    return recordings


@app.post("/participants", response_model=Participant)
async def create_participant(*, participant: ParticipantCreate, db: Session = Depends(get_db)):
    fresh_participant = crud.participant.create(db, participant)
    return fresh_participant


@app.get("/participants/{part_id}", response_model=Participant)
async def read_participant(part_id: int, db: Session = Depends(get_db)):
    recordings = crud.participant.get(db, part_id)
    return recordings


@app.delete("/participants/{part_id}", status_code=status.HTTP_200_OK)
async def delete_participant(*, part_id: int, db: Session = Depends(get_db)):
    crud.participant.remove(db_session=db, id=part_id)


@app.get("/participants/{part_id}/recordings", response_model=List[Recording])
async def read_recordings(part_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recordings = crud.recording.get_by_participant(db, participant_id=part_id, skip=skip, limit=limit)
    return recordings


@app.post("/participants/{part_id}/recordings", response_model=Recording)
async def create_recording(*, part_id: int, recording: RecordingCreate, db: Session = Depends(get_db)):
    fresh_recording = crud.recording.create_with_participant(db_session=db, obj_in=recording, participant_id=part_id)
    return fresh_recording


@app.get("/participants/{part_id}/recordings/{rec_id}", response_model=Recording)
async def read_recording(rec_id: int, db: Session = Depends(get_db)):
    recordings = crud.recording.get(db, rec_id)  # TODO perhaps check if rec_id and part_id match
    return recordings


@app.delete("/participants/{part_id}/recordings/{rec_id}", status_code=status.HTTP_200_OK)
async def delete_recording(*, rec_id: int, db: Session = Depends(get_db)):
    crud.recording.remove(db_session=db, id=rec_id)  # TODO perhaps check if rec_id and part_id match


@app.get("/participants/{part_id}/recordings/{rec_id}/files", response_model=List[File])
async def get_files(part_id: int, rec_id: int, db: Session = Depends(get_db)):
    fresh_files = crud.file.get_multi_for_recording(db_session=db, recording_id=rec_id)
    return fresh_files


@app.post("/participants/{part_id}/recordings/{rec_id}/files", response_model=File)
async def create_file(*, part_id: int, rec_id: int, file: FileCreate, db: Session = Depends(get_db)):
    fresh_file = crud.file.create_with_recording(db_session=db, obj_in=file, recording_id=rec_id)
    return fresh_file


@app.delete("/participants/{part_id}/recordings/{rec_id}/files/{file_id}", status_code=status.HTTP_200_OK)
async def delete_file(*, part_id: int, rec_id: int, file_id: int, db: Session = Depends(get_db)):
    crud.file.remove(db_session=db, id=file_id)


@app.get("/participants/{part_id}/recordings/{rec_id}/files/{file_id}/values", response_model=List[Value])
async def get_values(part_id: int, rec_id: int, file_id: int, db: Session = Depends(get_db)):
    fresh_value = crud.value.get_all_for_file(db_session=db, file_id=file_id)
    return fresh_value


@app.post("/participants/{part_id}/recordings/{rec_id}/files/{file_id}/values", response_model=Value)
async def create_value(*, part_id: int, rec_id: int, file_id: int, value: ValueCreate, db: Session = Depends(get_db)):
    fresh_value = crud.value.create_with_file(db_session=db, obj_in=value, file_id=file_id)
    return fresh_value


@app.get("/participants/{part_id}/recordings/{rec_id}/runs", response_model=List[Run])
async def get_runs(*, rec_id: int, db: Session = Depends(get_db)):
    runs = crud.run.get_all_for_recording(db_session=db, recording_id=rec_id)
    return runs


@app.post("/participants/{part_id}/recordings/{rec_id}/runs", response_model=Run)
async def start_run(*, rec_id: int, run: RunCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks):
    run.is_running = True
    fresh_run = crud.run.create_with_recoding(db_session=db, obj_in=run, recording_id=rec_id)
    background_tasks.add_task(Stream.start, fresh_run, db)
    return fresh_run


@app.get("/participants/{part_id}/recordings/{rec_id}/runs/{run_id}", response_model=Run)
async def get_run(*, run_id: int, db: Session = Depends(get_db)):
    run = crud.run.get(db_session=db, id=run_id)
    return run


@app.get("/participants/{part_id}/playlists", response_model=List[Playlist])
async def read_playlists(part_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    playlists = crud.playlist.get_by_participant(db, participant_id=part_id, skip=skip, limit=limit)
    return playlists


@app.post("/participants/{part_id}/playlists", response_model=Playlist)
async def create_playlist(*, part_id: int, playlist: PlaylistCreate, db: Session = Depends(get_db)):
    fresh_playlist = crud.playlist.create_with_participant(db, participant_id=part_id, obj_in=playlist)
    return fresh_playlist


@app.put("/participants/{part_id}/playlists", response_model=Playlist)
async def create_playlist(*, part_id: int, playlist: PlaylistUpdate, db: Session = Depends(get_db)):
    existing_playlist = crud.playlist.get_by_participant_and_type(db, part_id, playlist.type)
    if not existing_playlist:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_playlist = crud.playlist.update(db, db_obj=existing_playlist, obj_in=playlist)
    return updated_playlist


@app.get("/sensors", response_model=List[Sensor])
async def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.sensor.get_multi(db, skip=skip, limit=limit)
    return sensors


@app.post("/sensors", response_model=Sensor)
async def create_sensors(*, sensor: SensorCreate, db: Session = Depends(get_db)):
    fresh_sensor = crud.sensor.create(db, sensor)
    return fresh_sensor


@app.delete("/sensors/{sens_id}", status_code=status.HTTP_200_OK)
async def delete_file(*, sens_id: int, db: Session = Depends(get_db)):
    crud.sensor.remove(db_session=db, id=sens_id)
