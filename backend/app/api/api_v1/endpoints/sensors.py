from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app import crud
from backend.app import Sensor, SensorCreate
from backend.app.api import deps

router = APIRouter()


@router.get("/", response_model=List[Sensor])
async def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    sensors = crud.sensor.get_multi(db, skip=skip, limit=limit)
    return sensors


@router.post("/", response_model=Sensor)
async def create_sensors(*, sensor: SensorCreate, db: Session = Depends(deps.get_db)):
    fresh_sensor = crud.sensor.create(db, sensor)
    return fresh_sensor


@router.delete("/{sens_id}", status_code=status.HTTP_200_OK)
async def delete_file(*, sens_id: int, db: Session = Depends(deps.get_db)):
    crud.sensor.remove(db_session=db, id=sens_id)
