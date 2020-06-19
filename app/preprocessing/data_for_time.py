# This class provides the data type to start the data cleaning and is being returned by the stream class.


class DataForTime:

    # The class consists out of the following:
    #   The timestamp of the values
    #   The ID for the specific run
    #   The EDA value of this specific time
    #   The IBI value of this specific time
    #   The ACC values of 2 intervals (1 interval = 3 seconds?) in dictionaries before the time and of the current time
    #    => [0] is the oldest values while [-1] is the current ones,
    #    => if the stream just started, historic values might be x = 0, y = 0, z = 0.
    #   The Temp values of this specific time and of 30 seconds and 60 seconds after.

    def __init__(self):
        self.timestamp: int = 0
        self.runId: int = 0

        self.edaValue: float = 0
        self.ibiValue: float = 0
        self.tempValue: float = 0
        self.accValues = [{"x": 0, "y": 0, "z": 0}, {"x": 0, "y": 0, "z": 0}, {"x": 0, "y": 0, "z": 0}]

    def __str__(self):
        return str(self.timestamp) + \
               ", EDA: " + str(self.edaValue) + \
               ", IBI: " + str(self.ibiValue) + \
               ", TEMP: " + str(self.tempValue) + \
               ", ACC: " + str(self.accValues)
