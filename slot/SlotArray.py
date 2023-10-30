import queue
import threading
from slot.Data import Data


class SlotArray:
    def __init__(self, period: float, verbose: bool = False):
        # args
        self.period = period
        self.verbose = verbose

        # vars
        self.fifo = queue.Queue()
        self.slotArray = []

        # timer
        self.timer = None

    def stopHandle(self):
        self.clear()
        if self.verbose:
            print("[SlotArray] Kill timer.")
            print("[SlotArray] Clear slot array for reason: timeout.")

    def putFifo(self, data: Data):
        if self.timer is None or not self.timer.is_alive():
            self.timer = threading.Timer(self.period, self.stopHandle)
            self.timer.start()
            if self.verbose:
                print("[SlotArray] Start timer.")
        elif self.verbose:
            print("[SlotArray] Timer is already running.")

        self.fifo.put(data)

    def putArray(self, data: Data):
        self.slotArray.append(data)

    def clear(self):
        self.slotArray = []

    def print(self):
        for i in range(len(self.slotArray)):
            print(self.slotArray[i])
