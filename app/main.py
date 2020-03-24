from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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

class StartStop(BaseModel):
    start_stop: bool

class CreateSim(BaseModel):
    file: bool
    participant_id: str

@app.get("/simulations")
async def read_simulations():
    return [{"id": 1,
             "participantId": "DIMITRI",
             "running": True,
             "timeRunning": "13:40",
             "timeTotal": "12:40",
             "song": "test - song"
             },
            {"id": 2,
             "participantId": "ANJA",
             "running": False,
             "timeRunning": "00:00",
             "timeTotal": "29:30",
             "song": "-"
             }
            ]


@app.get("/simulations/{sim_id}")
async def read_simulation(sim_id: int):
    return {"id": sim_id,
            "participantId": "DIMITRI",
            "running": False,
            "timeRunning": "00:00",
            "timeTotal": "12:40",
            "song": "test - song"
            }


@app.post("/simulations", status_code=status.HTTP_201_CREATED)
async def create_simulation(create: CreateSim):
    #TODO: create Simulation record
    return {"id": 1}


@app.put("/simulations/{sim_id}", status_code=status.HTTP_200_OK)
async def start_stop_simulation(sim_id: int, start_stop: StartStop):
    #TODO: start/stop simulation
    return {"running": start_stop.start_stop}
