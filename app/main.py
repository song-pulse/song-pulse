from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://stream-pulse.netlify.com/",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/simulations")
async def create_simulation(file: int, part_id: int):
    return "OK"


@app.put("/simulations/{sim_id}")
async def start_stop_simulation(sim_id: int, running: bool):
    return "OK"
