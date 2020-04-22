from app import crud
from app.schemas.run import RunUpdate


class Stream:

    @staticmethod
    async def start(run, db_session):
        files = crud.file.get_multi_for_recording(db_session, recording_id=run.recording_id)
        for file in files:
            values = crud.value.get_all_for_file(db_session, file_id=file.id)
            for value in values:
                print(str(file.id) + ": @" + str(value.timestamp) + ": " + str(value.value))
        updated_run = RunUpdate(is_running=False, current_time=0)
        crud.run.update(db_session=db_session, db_obj=run, obj_in=updated_run)
