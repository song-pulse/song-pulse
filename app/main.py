from typing import List

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import crud
from app.database.session import Session
from app.schemas.recording import Recording
from app.schemas.participant import Participant

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
async def read_simulations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recordings = crud.participant.get_multi(db, skip=skip, limit=limit)
    return recordings


@app.get("/participants/{part_id}", response_model=Participant)
async def read_simulations(part_id: int, db: Session = Depends(get_db)):
    recordings = crud.participant.get(db, part_id)
    return recordings


@app.get("/recordings", response_model=List[Recording])
async def read_simulations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recordings = crud.recording.get_multi(db, skip=skip, limit=limit)
    return recordings


@app.get("/recordings/{rec_id}", response_model=Recording)
async def read_simulation(rec_id: int, db: Session = Depends(get_db)):
    recordings = crud.participant.get(db, rec_id)
    return recordings


@app.post("/recordings", status_code=status.HTTP_201_CREATED)
async def create_simulation(create: CreateSim):
    #TODO: create Simulation record
    return {"id": 1}


@app.put("/recordings/{rec_id}", status_code=status.HTTP_200_OK)
async def start_stop_simulation(sim_id: int, start_stop: StartStop):
    #TODO: start/stop simulation
    return {"running": start_stop.start_stop}
