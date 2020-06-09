from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import crud
from backend.app import Setting, SettingUpdate
from backend.app.api import deps

router = APIRouter()


@router.get("/", response_model=Setting)
async def read_setting(db: Session = Depends(deps.get_db)):
    setting = crud.setting.get(db, id=1)
    return setting


@router.put("/", response_model=Setting)
async def change_setting(*, setting: SettingUpdate, db: Session = Depends(deps.get_db)):
    existing_settings = crud.setting.get(db_session=db, id=1)
    if not existing_settings:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_setting = crud.setting.update(db_session=db, db_obj=existing_settings, obj_in=setting)
    return updated_setting