from unittest import TestCase

from app import crud
from app.api import deps
from app.processing.start.process_value import ProcessValue
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

        cls.add_files(recording.id, recording2.id)
        cls.acc_values = cls.add_values(cls.file_acc.id)
        cls.eda_values = cls.add_values(cls.file_eda.id)
        cls.ibi_values = cls.add_values(cls.file_ibi.id)

    @classmethod
    def add_files(cls, rec_id, rec2_id):
        cls.file_acc = crud.file.create_with_recording(db_session=cls.db_session,
                                                       obj_in=FileCreate(sensor_id=2, name="ACC"),
                                                       recording_id=rec_id)
        file_other_record = crud.file.create_with_recording(db_session=cls.db_session,
                                                            obj_in=FileCreate(sensor_id=2, name="ACC"),
                                                            recording_id=rec2_id)
        cls.file_ibi = crud.file.create_with_recording(db_session=cls.db_session,
                                                       obj_in=FileCreate(sensor_id=1, name="IBI"),
                                                       recording_id=rec_id)
        cls.file_eda = crud.file.create_with_recording(db_session=cls.db_session,
                                                       obj_in=FileCreate(sensor_id=4, name="EDA"),
                                                       recording_id=rec_id)
        file_other_name = crud.file.create_with_recording(db_session=cls.db_session,
                                                          obj_in=FileCreate(sensor_id=3, name="BLA"),
                                                          recording_id=rec_id)
        cls.files = [cls.file_acc, file_other_record, file_other_name, cls.file_ibi, cls.file_eda]

    @classmethod
    def add_values(cls, file_acc_id):
        value_newer = crud.value.create_with_file(db_session=cls.db_session,
                                                  obj_in=ValueCreate(timestamp=210, value1=1, value2=2, value3=3),
                                                  file_id=file_acc_id)
        cls.value_current = crud.value.create_with_file(db_session=cls.db_session,
                                                        obj_in=ValueCreate(timestamp=200, value1=4, value2=5, value3=6),
                                                        file_id=file_acc_id)
        value_old1 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=190, value1=7, value2=8, value3=9),
                                                 file_id=file_acc_id)
        value_old2 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=180, value1=10, value2=11, value3=12),
                                                 file_id=file_acc_id)
        value_old3 = crud.value.create_with_file(db_session=cls.db_session,
                                                 obj_in=ValueCreate(timestamp=170, value1=13, value2=14, value3=15),
                                                 file_id=file_acc_id)
        return [value_newer, cls.value_current, value_old1, value_old2, value_old3]

    @classmethod
    def tearDownClass(cls) -> None:
        for val in cls.acc_values:
            crud.value.remove(db_session=cls.db_session, id=val.id)

        for val in cls.ibi_values:
            crud.value.remove(db_session=cls.db_session, id=val.id)

        for val in cls.eda_values:
            crud.value.remove(db_session=cls.db_session, id=val.id)

        for file in cls.files:
            crud.file.remove(db_session=cls.db_session, id=file.id)

        for rec in cls.recordings:
            crud.recording.remove(db_session=cls.db_session, id=rec.id)

    def test_historic_acc(self) -> None:
        db_session = next(deps.get_db())

        values = ProcessValue.get_historic_acc(db_session, self.value_current.timestamp, self.rec_id, 2)

        self.assertEqual(2, len(values))
        self.assertEqual(190, values[0].timestamp)
        self.assertEqual(7, values[0].value1)
        self.assertEqual(8, values[0].value2)
        self.assertEqual(9, values[0].value3)
        self.assertEqual(180, values[1].timestamp)
        self.assertEqual(10, values[1].value1)
        self.assertEqual(11, values[1].value2)
        self.assertEqual(12, values[1].value3)

    def test_historic_ibi(self) -> None:
        db_session = next(deps.get_db())

        values = ProcessValue.get_historic_ibi(db_session, self.value_current.timestamp, self.rec_id, 2)

        self.assertEqual(2, len(values))
        self.assertEqual(190, values[0].timestamp)
        self.assertEqual(7, values[0].value1)
        self.assertEqual(180, values[1].timestamp)
        self.assertEqual(10, values[1].value1)

    def test_historic_eda(self) -> None:
        db_session = next(deps.get_db())

        values = ProcessValue.get_historic_eda(db_session, self.value_current.timestamp, self.rec_id, 2)

        self.assertEqual(2, len(values))
        self.assertEqual(190, values[0].timestamp)
        self.assertEqual(7, values[0].value1)
        self.assertEqual(180, values[1].timestamp)
        self.assertEqual(10, values[1].value1)

    def test_convert_to_data_for_time(self) -> None:
        val = TimestampValues(timestamp=self.value_current.timestamp, eda=1.1, ibi=2.2, temp=3.3, acc_x=4.4,
                              acc_y=5.5,
                              acc_z=6.6)
        data_for_time = ProcessValue.convert_to_data_for_time(db_session=self.db_session, values=val,
                                                              rec_id=self.rec_id, run_id=1)
        self.assertEqual(val.timestamp, data_for_time.timestamp)

        self.assertEqual(3, len(data_for_time.edaValues))
        self.assertEqual(7.0, data_for_time.edaValues[2])
        self.assertEqual(10.0, data_for_time.edaValues[1])
        self.assertEqual(13.0, data_for_time.edaValues[0])

        self.assertEqual(3, len(data_for_time.ibiValues))
        self.assertEqual(7.0, data_for_time.ibiValues[2])
        self.assertEqual(10.0, data_for_time.ibiValues[1])
        self.assertEqual(13.0, data_for_time.ibiValues[0])

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

        self.assertEqual(1, len(data_for_time.edaValues))
        self.assertEqual(13.0, data_for_time.edaValues[0])

        self.assertEqual(1, len(data_for_time.ibiValues))
        self.assertEqual(13.0, data_for_time.ibiValues[0])

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
        self.assertEqual(0, len(data_for_time.edaValues))
        self.assertEqual(0, len(data_for_time.ibiValues))
        self.assertEqual(val.temp, data_for_time.tempValue)
        self.assertEqual(3, len(data_for_time.accValues))
        self.assertEqual({'x': 4.4, 'y': 5.5, 'z': 6.6}, data_for_time.accValues[2])
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, data_for_time.accValues[1])
        self.assertEqual({'x': 0, 'y': 0, 'z': 0}, data_for_time.accValues[0])
