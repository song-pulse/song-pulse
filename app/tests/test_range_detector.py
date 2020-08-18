from unittest import TestCase

from app import crud
from app.api import deps
from app.processing.min_max_detector import MinMaxDetector
from app.schemas.recording import RecordingCreate
from app.schemas.run import RunCreate


class TestRangeDetector(TestCase):

    def test_min_max_detection(self) -> None:
        db_session = next(deps.get_db())
        recording = crud.recording.create_with_participant(db_session=db_session,
                                                           obj_in=RecordingCreate(name="test"), participant_id=1)
        run = crud.run.create_with_recoding(db_session=db_session,
                                            obj_in=RunCreate(), recording_id=recording.id)

        detector = MinMaxDetector()
        eda_tendency, mean_rr_tendency, prr_20_tendency = detector.detect(db_session=db_session, eda_value=1.1234,
                                                                          mean_rr_value=0.99876, prr_20_value=80,
                                                                          run_id=run.id)
        self.assertEqual(2, eda_tendency)
        self.assertEqual(0, mean_rr_tendency)
        self.assertEqual(0, prr_20_tendency)

        eda_tendency, mean_rr_tendency, prr_20_tendency = detector.detect(db_session=db_session, eda_value=1.0012,
                                                                          mean_rr_value=0.9832, prr_20_value=100,
                                                                          run_id=run.id)
        self.assertEqual(0, eda_tendency)
        self.assertEqual(2, mean_rr_tendency)
        self.assertEqual(0, prr_20_tendency)

        eda_tendency, mean_rr_tendency, prr_20_tendency = detector.detect(db_session=db_session, eda_value=1.1,
                                                                          mean_rr_value=0.9921, prr_20_value=90,
                                                                          run_id=run.id)
        self.assertEqual(1, eda_tendency)
        self.assertEqual(1, mean_rr_tendency)
        self.assertEqual(1, prr_20_tendency)

        eda_tendency, mean_rr_tendency, prr_20_tendency = detector.detect(db_session=db_session, eda_value=1.1,
                                                                          mean_rr_value=0.9921, prr_20_value=70,
                                                                          run_id=run.id)
        self.assertEqual(1, eda_tendency)
        self.assertEqual(1, mean_rr_tendency)
        self.assertEqual(2, prr_20_tendency)
