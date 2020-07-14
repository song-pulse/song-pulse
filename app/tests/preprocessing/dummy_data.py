class Settings:
    def __init__(self):
        self.duration = 3
        self.temp_latency = 2
        self.acc_threshold = 18
        self.eda_threshold = 0.3
        self.ibi_threshold = 0.4
        self.prr_threshold = 0.5
        self.stress_threshold = 0.5


class Data:
    def __init__(self):
        self.acc_values = []
