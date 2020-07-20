from app import crud
from app.preprocessing.data_for_time import DataForTime
from app.preprocessing.learning_wrapper import LearningWrapper
from app.spotify.song_queuer import queue_song_if_needed


class Stream:

    @staticmethod
    def start(part_id, rec_id, run_id, spotify_username):
        learning = LearningWrapper()
        # The values for the different sensors are being stored in those lists.
        eda_data = []
        ibi_data = []
        acc_data = []
        temp_data = []
        bvp_data = []

        db_session = learning.get_db_session()
        # Get the files from the recording.
        files = crud.file.get_multi_for_recording(db_session, recording_id=rec_id)

        # Iterate over the files.
        for file in files:

            # Get the values out of the file
            values = crud.value.get_all_for_file(db_session, file_id=file.id)

            # Sort the values in the file so that they are sorted according to their timestamp.
            values.sort(key=lambda x: x.timestamp)

            # Store the file in the correct variable according to their sensor ID.
            if file.sensor.name.lower() == "TEMP".lower():
                temp_data = values
            elif file.sensor.name.lower() == "EDA".lower():
                eda_data = values
            elif file.sensor.name.lower() == "BVP".lower():
                bvp_data = values
            elif file.sensor.name.lower() == "ACC".lower():
                acc_data = values
            elif file.sensor.name.lower() == "IBI".lower():
                ibi_data = values

        # Iterate over the eda file with its values
        for value in eda_data:
            data_for_time_object = Stream.create_data_for_time_object(value, acc_data, bvp_data, eda_data, ibi_data,
                                                                      run_id, temp_data)
            action = learning.run(data_for_time_object, part_id)
            result = queue_song_if_needed(db_session, data_for_time_object, action, part_id, run_id, spotify_username)
            crud.result.create_with_run(db_session=db_session, obj_in=result, run_id=run_id)

    # This methods creates a data object for a given time stamp.
    # This object can then be given to the data cleaning for processing the data.
    @staticmethod
    def create_data_for_time_object(value, acc_data, bvp_data, eda_data, ibi_data, run_id, temp_data):
        data_for_time = DataForTime()

        # first add the run ID plus the time stamp
        data_for_time.runId = run_id
        data_for_time.timestamp = value.timestamp

        # Add the values for the specific time.
        data_for_time.edaValue = value.value1

        # Iterate over the bvp values and add the value at the given time stamp.
        for bvpValue in bvp_data:
            if bvpValue.timestamp == value.timestamp:
                data_for_time.bvpValue = bvpValue.value1

        # Iterate over the ibi values and add the value at the given time stamp.
        for ibiValue in ibi_data:
            if ibiValue.timestamp == value.timestamp:
                data_for_time.bvpValue = ibiValue.value1

        # The intervals are the data points for the acc before the time stamp.
        # They are later needed for the data cleaning.
        acc_interval1 = {"x": 0, "y": 0, "z": 0}
        acc_interval2 = {"x": 0, "y": 0, "z": 0}
        # Iterate over the acc values and add the value at the given time stamp plus of two intervals from before.
        for accValue in acc_data:
            if accValue.timestamp == value.timestamp:
                data_for_time.accValues[0] = (acc_interval1["x"], acc_interval1["y"], acc_interval1["z"])
                data_for_time.accValues[1] = (acc_interval2["x"], acc_interval2["y"], acc_interval2["z"])
                data_for_time.accValues[2] = (accValue.value1, accValue.value2, accValue.value3)
            else:
                acc_interval1 = acc_interval2
                acc_interval2 = {"x": accValue.value1, "y": accValue.value2, "z": accValue.value3}

        # Iterate over the temp values and add the value at the given time stamp.
        for tempValue in temp_data:
            if tempValue.timestamp == value.timestamp:
                data_for_time.tempValue = tempValue.value1

        return data_for_time
