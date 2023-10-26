from EDataType import DataType


class Data:
    def __init__(self, dataType: DataType, value):
        self.dataType = dataType
        self.value = value

    def print(self):
        print(self.dataType, self.value)
