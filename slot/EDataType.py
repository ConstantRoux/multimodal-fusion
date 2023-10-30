from enum import Enum


class DataType(Enum):
    ACTION = 0
    SHAPE = 1
    COLOR = 2
    POSITION = 3


class ActionType(Enum):
    ADD = 0
    MOVE = 1
    DELETE = 2


class ShapeType(Enum):
    RECTANGLE = 0
    CIRCLE = 1
    TRIANGLE = 2


class ColorType(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
