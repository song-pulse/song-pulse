from app.core.celery_app import celery_app
from app.preprocessing.stream import Stream


@celery_app.task(acks_late=True)
def run(part_id: int, rec_id: int, run_id: int):
    Stream.start(part_id, rec_id, run_id)
