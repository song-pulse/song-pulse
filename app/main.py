from typing import List

from fastapi import Depends, FastAPI, status, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import crud
from app.parser.value_parser import parse_and_save_values
from app.database.session import Session
from app.schemas.sensor import Sensor, SensorCreate
from app.schemas.file import File as OwnFile, FileCreate
from app.schemas.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from app.schemas.recording import Recording, RecordingCreate
from app.schemas.participant import Participant, ParticipantCreate

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


class StartStop(BaseModel):
    start_stop: bool


class CreateSim(BaseModel):
    file: bool
    participant_id: str


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
    crud.participant.remove(db_session=db, id=part_id) # TODO remove all other data of this participant


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
    recordings = crud.recording.get(db, rec_id) # TODO perhaps check if rec_id and part_id match
    return recordings


@app.delete("/participants/{part_id}/recordings/{rec_id}", status_code=status.HTTP_200_OK)
async def delete_recording(*, rec_id: int, db: Session = Depends(get_db)):
    crud.recording.remove(db_session=db, id=rec_id) # TODO perhaps check if rec_id and part_id match


@app.post("/participants/{part_id}/recordings/{rec_id}/sensors/{sensor_id}", response_model=OwnFile)
async def create_file_values(part_id: int, rec_id: int, sensor_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    fresh_file = crud.file.create_with_recording(db_session=db, obj_in=FileCreate(sensor_id=sensor_id, name=file.filename), recording_id=rec_id)
    await parse_and_save_values(db_session=db, file_id=fresh_file.id, file=file.file) # TODO what to do with this?
    return fresh_file

# TODO replace existing values!


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
