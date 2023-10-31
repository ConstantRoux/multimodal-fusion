from slot.EDataType import ShapeType, ColorType


class Object:
    def __init__(self, objectID: int, shapeType: ShapeType, colorType: ColorType, x: int, y: int, size: int):
        # args
        self.objectID = objectID
        self.shapeType = shapeType
        self.colorType = colorType
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return str(self.objectID) + " " + str(self.shapeType) + " " + str(self.colorType) + " " + str(self.x) + " " + str(self.y) + " " + str(self.size)
