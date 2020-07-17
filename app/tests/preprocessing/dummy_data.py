class Settings:
    def __init__(self):
        self.duration = 3
        self.temp_latency = 2
        self.acc_threshold = 0.2
        self.eda_threshold = 2.3
        self.ibi_threshold = 0.4
        self.prr_threshold = 0.5
        self.stress_threshold = 0.5


class Data:
    def __init__(self, movement=True):
        if movement:
            self.accValues = [{'x': 1, 'y': 1, 'z': 10},
                              {'x': 1, 'y': 2, 'z': 10},
                              {'x': 0, 'y': 1, 'z': 20},
                              {'x': -1, 'y': 0, 'z': 10}]

        else:
            self.accValues = [{'x': 1, 'y': 1, 'z': 1},
                              {'x': 1, 'y': 2, 'z': 1},
                              {'x': 0, 'y': 1, 'z': 2},
                              {'x': -1, 'y': 0, 'z': 1}]
