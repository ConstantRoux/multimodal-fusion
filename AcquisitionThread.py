import threading


class AcquisitionThread:
    def __init__(self, period):
        self.started = False
        self.period = period
        