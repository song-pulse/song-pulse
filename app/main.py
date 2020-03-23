from fastapi import FastAPI

app = FastAPI()


@app.get("/simulations")
async def read_simulations():
    return [{"id": 1,
             "participantId": 2,
             "running": False,
             "timeRunning": "00:00",
             "timeTotal": "12:40",
             "song": "test - song"
             },
            {"id": 1,
             "participantId": 2,
             "running": False,
             "timeRunning": "00:00",
             "timeTotal": "12:40",
             "song": "test - song"
             }
            ]


@app.get("/simulations/{sim_id}")
async def read_simulation(sim_id: int):
    return {"id": sim_id,
            "participantId": 2,
            "running": False,
            "timeRunning": "00:00",
            "timeTotal": "12:40",
            "song": "test - song"
            }


@app.post("/simulations")
async def create_simulation(file: int, part_id: int):
    return "OK"


@app.put("/simulations/{sim_id}")
async def start_stop_simulation(sim_id: int, running: bool):  # TODO start or stop
    return "OK"
