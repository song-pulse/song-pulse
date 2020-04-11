from tempfile import SpooledTemporaryFile
from app import crud
from app.database.session import Session
from app.schemas.value import ValueCreate
import re


async def parse_and_save_values(db_session: Session,file_id: int, file: SpooledTemporaryFile):
    # TODO: Build something less hacky
    row_no = 0
    timestamp = 0
    frequency = 0
    line = file.readline()
    while line:
        line = re.sub('[^0-9.]', '', line.decode('utf-8'))
        if row_no == 0:
            timestamp = float(line)
        elif row_no == 1:
            frequency = float(line)
        else:
            value = float(line)
            crud.value.create_with_file(db_session=db_session, obj_in=ValueCreate(timestamp=timestamp, value=value), file_id=file_id)
            timestamp = timestamp + frequency
        row_no = row_no + 1
        line = file.readline()
