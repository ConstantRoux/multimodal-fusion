from SlotData import dataOrd, DataType


class SlotArray:
    def __init__(self):
        self.slotArray = [None] * dataOrd

    def fill(self, dataType, dataValue):
        self.slotArray[dataType] = dataValue

    def clear(self):
        self.slotArray = [None] * dataOrd

    def print(self):
        for i in range(dataOrd):
            if self.slotArray[i] is not None:
                print(self.slotArray[i])
