from app import crud
from app.preprocessing.DataForTime import DataForTime
from app.schemas.run import RunUpdate


class Stream:

    @staticmethod
    async def start(run, db_session):
        # The values for the different sensors are being stored in those lists.
        eda_data = []
        ibi_data = []
        acc_data = []
        temp_data = []
        bvp_data = []

        # The intervals are the data points for the acc before the time stamp.
        # They are later needed for the data cleaning.
        acc_interval1 = None
        acc_interval2 = None

        # Get the files from the recording.
        files = crud.file.get_multi_for_recording(db_session, recording_id=run.recording_id)

        # Iterate over the files.
        for file in files:

            # Get the values out of the file
            values = crud.value.get_all_for_file(db_session, file_id=file.id)

            # Sort the values in the file so that they are sorted according to their timestamp.
            values.list.sort(key=values.timestamp)

            # Store the file in the correct variable according to their sensor ID.
            if file.sensor_id == 1:
                temp_data = values
            elif file.sensor_id == 2:
                eda_data = values
            elif file.sensor_id == 3:
                bvp_data = values
            elif file.sensor_id == 4:
                acc_data = values
            elif file.sensor_id == 5:
                ibi_data = values

        # Iterate over the eda file with its values
        for value in eda_data:
            data_for_time_object = Stream.createdatafortimeobject(value, acc_data, acc_interval1, acc_interval2,
                                                                  bvp_data, eda_data,
                                                                  ibi_data, run,
                                                                  temp_data)
            print(data_for_time_object)

        updated_run = RunUpdate(is_running=False, current_time=0)
        crud.run.update(db_session=db_session, db_obj=run, obj_in=updated_run)

    # This methods creates a data object for a given time stamp.
    # This object can then be given to the data cleaning for processing the data.
    @staticmethod
    async def createdatafortimeobject(value, acc_data, acc_interval1, acc_interval2, bvp_data, eda_data, ibi_data, run,
                                      temp_data):
        data_for_time = DataForTime()

        # first add the run ID plus the time stamp
        data_for_time.runId = run.id
        data_for_time.timestamp = value.timestamp

        # Add the values for the specific time.
        data_for_time.edaValue = value.value

        # Iterate over the bvp values and add the value at the given time stamp.
        for bvpValue in bvp_data:
            if bvpValue.timestamp == value.timestamp:
                data_for_time.bvpValue = bvpValue.value

        # Iterate over the ibi values and add the value at the given time stamp.
        for ibiValue in ibi_data:
            if ibiValue.timestamp == value.timestamp:
                data_for_time.bvpValue = ibiValue.value

        # Iterate over the acc values and add the value at the given time stamp plus of two intervals from before.
        for accValue in acc_data:
            if accValue.timestamp == value.timestamp:
                data_for_time.accValues.append(acc_interval1)
                data_for_time.accValues.append(acc_interval2)
                data_for_time.accValues.append(accValue.value)
            else:
                acc_interval1 = acc_interval2
                acc_interval2 = accValue.value

        # Iterate over the temp values and add the value at the given time stamp.
        for tempValue in temp_data:
            if tempValue.timestamp == value.timestamp:
                data_for_time.tempValue = tempValue.value

        return data_for_time
