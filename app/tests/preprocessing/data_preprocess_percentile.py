from unittest import TestCase

from app import crud
from app.api import deps
from app.processing.indicator_calculation import compute_prr20, compute_mean_rr, compute_mean_eda, majority_vote
from app.processing.start.process_value import ProcessValue
from app.schemas.file import FileCreate
from app.schemas.recording import RecordingCreate
from app.schemas.run import RunCreate
from app.schemas.tendency import TendencyCreate
from app.schemas.timestamp_values import TimestampValues
from app.schemas.value import ValueCreate


class TestLearningWrapper(TestCase):

    def test_compute_prr20_first(self) -> None:
        self.assertEqual(0, compute_prr20([0.93456432]))

    def test_compute_prr20(self) -> None:
        # the last change is very big, so it we get 3/4
        self.assertEqual(75, compute_prr20([0.93456432, 1.0543789, 0.983456, 0.99213456, 1.2452345]))

    def test_compute_prr20_more(self) -> None:
        self.assertEqual(71.42857142857143, compute_prr20([0.8, 1.0, 1.0, 0.9, 1.2, 0.8, 1.2, 1.2]))

    def test_compute_mean_rr_first(self) -> None:
        self.assertEqual(0.93456432, compute_mean_rr([0.93456432]))

    def test_compute_mean_rr(self) -> None:
        self.assertEqual(1.041953656, compute_mean_rr([0.93456432, 1.0543789, 0.983456, 0.99213456, 1.2452345]))

    def test_compute_mean_rr_more(self) -> None:
        self.assertEqual(1.0125, compute_mean_rr([0.8, 1.0, 1.0, 0.9, 1.2, 0.8, 1.2, 1.2]))

    def test_compute_mean_eda_first(self) -> None:
        self.assertEqual(0.93456432, compute_mean_eda([0.93456432]))

    def test_compute_mean_eda(self) -> None:
        self.assertEqual(1.041953656, compute_mean_eda([0.93456432, 1.0543789, 0.983456, 0.99213456, 1.2452345]))

    def test_compute_mean_eda_more(self) -> None:
        self.assertEqual(1.0125, compute_mean_eda([0.8, 1.0, 1.0, 0.9, 1.2, 0.8, 1.2, 1.2]))

    def test_majority_vote_relaxed(self) -> None:
        db_session = next(deps.get_db())
        recording = crud.recording.create_with_participant(db_session=db_session,
                                                           obj_in=RecordingCreate(name="test"), participant_id=1)
        run = crud.run.create_with_recoding(db_session=db_session,
                                            obj_in=RunCreate(), recording_id=recording.id)

        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=100, eda=1, mean_rr=1, prr_20=1), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=110, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=120, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=130, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=140, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=150, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=160, eda=0, mean_rr=1, prr_20=0), run_id=run.id)

        self.assertEqual(0, majority_vote(db_session=db_session, run_id=run.id))

    def test_majority_vote_balanced(self) -> None:
        db_session = next(deps.get_db())
        recording = crud.recording.create_with_participant(db_session=db_session,
                                                           obj_in=RecordingCreate(name="test"), participant_id=1)
        run = crud.run.create_with_recoding(db_session=db_session,
                                            obj_in=RunCreate(), recording_id=recording.id)

        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=100, eda=0, mean_rr=0, prr_20=0), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=110, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=120, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=130, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=140, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=150, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=160, eda=0, mean_rr=1, prr_20=1), run_id=run.id)

        self.assertEqual(1, majority_vote(db_session=db_session, run_id=run.id))

    def test_majority_vote_stressed(self) -> None:
        db_session = next(deps.get_db())
        recording = crud.recording.create_with_participant(db_session=db_session,
                                                           obj_in=RecordingCreate(name="test"), participant_id=1)
        run = crud.run.create_with_recoding(db_session=db_session,
                                            obj_in=RunCreate(), recording_id=recording.id)

        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=100, eda=0, mean_rr=0, prr_20=0), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=110, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=120, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=130, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=140, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=150, eda=0, mean_rr=1, prr_20=2), run_id=run.id)
        crud.tendency.create_with_run(db_session=db_session,
                                      obj_in=TendencyCreate(timestamp=160, eda=0, mean_rr=2, prr_20=2), run_id=run.id)

        self.assertEqual(2, majority_vote(db_session=db_session, run_id=run.id))
