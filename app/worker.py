from app.core.celery_app import celery_app
from app.preprocessing.process_value import ProcessValue
from app.preprocessing.stream import Stream
from app.schemas.timestamp_values import TimestampValues


@celery_app.task(acks_late=True)
def run(part_id: int, rec_id: int, run_id: int, timestamp: int, eda: float, ibi: float, temp: float, acc_x: float, acc_y: float, acc_z: float):
    if timestamp < 0:
        Stream.start(part_id, rec_id, run_id)
    else:
        values = TimestampValues(timestamp=timestamp, eda=eda, ibi=ibi, temp=temp, acc_x=acc_x, acc_y=acc_y, acc_z=acc_z)
        ProcessValue.single_value(part_id, rec_id, run_id, values)
