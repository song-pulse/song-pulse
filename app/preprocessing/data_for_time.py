# This class provides the data type to start the data cleaning and is being returned by the stream class.


class DataForTime:

    # The class consists out of the following:
    #   The timestamp of the values
    #   The ID for the specific run
    #   The EDA value of this specific time
    #   The IBI value of this specific time
    #   The ACC values of 2 intervals (1 interval = 3 seconds?) before the time and of this specific time.
    #   The Temp values of this specific time and of 30 seconds and 60 seconds after.
    #   The BVP values of this specific time

    def __init__(self):
        self.timestamp = 0
        self.runId = 0

        self.edaValue = 0
        self.ibiValue = 0
        self.accValues = []
        self.tempValue = 0
        self.bvpValue = 0

    def __str__(self):
        return str(self.timestamp) + " " + str(self.edaValue)  # TODO extend
