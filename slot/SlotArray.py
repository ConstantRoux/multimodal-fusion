from EDataType import data_ord
import queue


class SlotArray:
    def __init__(self):
        self.fifo = queue.Queue()
        self.slotArray = [None] * data_ord

    def clear(self):
        self.slotArray = [None] * data_ord

    def print(self):
        for i in range(data_ord):
            if self.slotArray[i] is not None:
                print(self.slotArray[i])
