import threading
import time
from slot.SlotArray import SlotArray
from slot.Data import Data
from slot.EDataType import DataType


class AcquisitionThread(threading.Thread):
    def __init__(self, slotArray: SlotArray, period: float, verbose: bool = False):
        # inheritance
        super(AcquisitionThread, self).__init__(target=self.callback)

        # get args
        self.slotArray = slotArray
        self.period = period
        self.verbose = verbose

        # variables
        self.started = False
        self.elapsed_time = 0

        # launch thread
        self.start()

        # verbose
        if self.verbose:
            print("Thread Acquisition launched")

    def stopCycle(self, reason: str = ""):
        # reset timer
        self.started = False
        self.elapsed_time = 0

        # reset slot array
        self.slotArray.clear()

        # verbose
        if self.verbose:
            print("stop cycle for reason:", reason)

    def callback(self):
        self.elapsed_time = 0
        while True:
            # measure time
            t_start = time.time()

            # get list of data
            data = [Data(DataType.ACTION, 0)]
            # TODO

            # if there is a new data
            if len(data) == 0:
                for i in range(len(data)):
                    self.slotArray.fifo.put(data[i])

                # if there is not a running cycle
                if not self.started:
                    self.started = True

            # if a cycle has started
            if self.started:
                # measure elapsed time
                self.elapsed_time += time.time() - t_start
                if self.elapsed_time >= self.period:
                    # stop cycle
                    self.stopCycle("end of period")

            # wait to free cpu time
            time.sleep(0.01)
