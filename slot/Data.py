from slot.EDataType import DataType


class Data:
    def __init__(self, dataType: DataType, value, confidence: float):
        self.dataType = dataType
        self.value = value  # can be a subtype or coordinates
        self.confidence = confidence

    def __str__(self):
        return str(self.dataType) + " " + str(self.value) + " " + str(self.confidence)
