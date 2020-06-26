from unittest import TestCase

from app import crud
from app.api import deps
from app.preprocessing.process_value import ProcessValue
from app.schemas.file import FileCreate
from app.schemas.recording import RecordingCreate
from app.schemas.timestamp_values import TimestampValues
from app.schemas.value import ValueCreate


class TestLearningWrapper(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.db_session = next(deps.get_db())
        recording = crud.recording.create_with_participant(db_session=cls.db_session,
                                                           obj_in=RecordingCreate(name="test"), participant_id=1)
        recording2 = crud.recording.create_with_participant(db_session=cls.db_session,
                                                            obj_in=RecordingCreate(name="test2"), participant_id=1)
        cls.recordings = [recording, recording2]
        cls.rec_id = recording.id

        cls.file_test = crud.file.create_with_recording(db_session=cls.db_session,
                                                        obj_in=FileCreate(sensor_id=2, name="ACC"),
                                                        recording_id=cls.rec_id)
        file_other_record = crud.file.create_with_recording(db_session=cls.db_session,
                                                            obj_in=FileCreate(sensor_id=1, name="ACC"),
                                                            recording_id=recording2.id)

        file_other_name = crud.file.create_with_recording(db_session=cls.db_session,
                                                          obj_in=FileCreate(sensor_id=3, name="BLA"),
                                                          recording_id=cls.rec_id)
        cls.files = [cls.file_test, file_other_record, file_other_name]

        value_newer = crud.value.create_with_file(db_session=cls.db_session,
                                                  obj_in=ValueCreate(timestamp=210, value1=1, value2=2, value3=3),
                                                  file_id=cls.file_test.id)
        cls.value_current = crud.value.create_with_file(db_session=cls.db_session,
                                                        obj_in=ValueCreate(timestamp=200, value1=4, value2=5, value3=6),
                                                        file_id=cls.file_test.id)
        value_old1 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=190, value1=7, value2=8, value3=9),
                                                 file_id=cls.file_test.id)
        value_old2 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=180, value1=10, value2=11, value3=12),
                                                 file_id=cls.file_test.id)
        value_old3 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=170, value1=13, value2=14, value3=15),
                                                 file_id=cls.file_test.id)
        cls.values = [value_newer, cls.value_current, value_old1, value_old2, value_old3]

    @classmethod
    def tearDownClass(cls) -> None:
        for val in cls.values:
            crud.value.remove(db_session=cls.db_session, id=val.id)

        for file in cls.files:
            crud.file.remove(db_session=cls.db_session, id=file.id)

        for rec in cls.recordings:
            crud.recording.remove(db_session=cls.db_session, id=rec.id)

    def test_calculate_baseline(self) -> None:
        db_session = next(deps.get_db())

        values = ProcessValue.get_historic_acc(db_session, self.value_current.timestamp, self.rec_id)

        self.assertEqual(2, len(values))
        self.assertEqual(190, values[0].timestamp)
        self.assertEqual(7, values[0].value1)
        self.assertEqual(8, values[0].value2)
        self.assertEqual(9, values[0].value3)
        self.assertEqual(180, values[1].timestamp)
        self.assertEqual(10, values[1].value1)
        self.assertEqual(11, values[1].value2)
        self.assertEqual(12, values[1].value3)

    def test_convert_to_data_for_time(self) -> None:
        val = TimestampValues(timestamp=self.value_current.timestamp, eda=1.1, ibi=2.2, temp=3.3, acc_x=4.4,
                              acc_y=5.5,
                              acc_z=6.6)
        data_for_time = ProcessValue.convert_to_data_for_time(db_session=self.db_session, values=val,
                                                              rec_id=self.rec_id, run_id=1)
        self.assertEqual(val.timestamp, data_for_time.timestamp)
        self.assertEqual(val.eda, data_for_time.edaValue)
        self.assertEqual(val.ibi, data_for_time.ibiValue)
        self.assertEqual(val.temp, data_for_time.tempValue)
        self.assertEqual(3, len(data_for_time.accValues))
        self.assertEqual({'x': 4.4, 'y': 5.5, 'z': 6.6}, data_for_time.accValues[2])
        self.assertEqual({'x': 7, 'y': 8, 'z': 9}, data_for_time.accValues[1])
        self.assertEqual({'x': 10, 'y': 11, 'z': 12}, data_for_time.accValues[0])

    def test_convert_to_data_for_time_one_historic(self) -> None:
        val = TimestampValues(timestamp=180, eda=1.1, ibi=2.2, temp=3.3, acc_x=4.4, acc_y=5.5,
                              acc_z=6.6)
        data_for_time = ProcessValue.convert_to_data_for_time(db_session=self.db_session, values=val,
                                                              rec_id=self.rec_id, run_id=1)
        self.assertEqual(val.timestamp, data_for_time.timestamp)
        self.assertEqual(val.eda, data_for_time.edaValue)
        self.assertEqual(val.ibi, data_for_time.ibiValue)
        self.assertEqual(val.temp, data_for_time.tempValue)
        self.assertEqual(3, len(data_for_time.accValues))
        self.assertEqual({'x': 4.4, 'y': 5.5, 'z': 6.6}, data_for_time.accValues[2])
        self.assertEqual({'x': 13, 'y': 14, 'z': 15}, data_for_time.accValues[1])
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, data_for_time.accValues[0])

    def test_convert_to_data_for_time_no_historic(self) -> None:
        val = TimestampValues(timestamp=170, eda=1.1, ibi=2.2, temp=3.3, acc_x=4.4, acc_y=5.5,
                              acc_z=6.6)
        data_for_time = ProcessValue.convert_to_data_for_time(db_session=self.db_session, values=val,
                                                              rec_id=self.rec_id, run_id=1)
        self.assertEqual(val.timestamp, data_for_time.timestamp)
        self.assertEqual(val.eda, data_for_time.edaValue)
        self.assertEqual(val.ibi, data_for_time.ibiValue)
        self.assertEqual(val.temp, data_for_time.tempValue)
        self.assertEqual(3, len(data_for_time.accValues))
        self.assertEqual({'x': 4.4, 'y': 5.5, 'z': 6.6}, data_for_time.accValues[2])
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, data_for_time.accValues[1])
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, data_for_time.accValues[0])
