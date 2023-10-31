import queue
import threading
from process.Command import Command
from slot.Data import Data


class SlotArray:
    def __init__(self, period: float, verbose: bool = False):
        # args
        self.period = period
        self.verbose = verbose

        # vars
        self.fifo = queue.Queue()
        self.slotArray = []
        self.cmd = Command()

        # timer
        self.timer = None

    def stopHandle(self):
        self.clear("timeout")
        if self.verbose:
            print("[SlotArray] Kill timer.")

    def stop(self, reason: str):
        if self.timer is not None:
            self.timer.cancel()
            self.clear(reason)
            if self.verbose:
                print("[SlotArray] Kill timer.")

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

    def clear(self, reason: str):
        self.slotArray = []
        with self.fifo.mutex:
            self.fifo.queue.clear()
        if self.verbose:
            print("[SlotArray] Clear slot array for reason:", reason + ".")

    def print(self):
        for i in range(len(self.slotArray)):
            print(self.slotArray[i])
