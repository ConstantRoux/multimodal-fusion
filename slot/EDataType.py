from enum import Enum


data_ord = 5


class DataType(Enum):
    ACTION = 0
    SHAPE = 1
    COLOR = 2
    POSITION_1 = 3
    POSITION_2 = 4


class ActionType(Enum):
    ADD = 0
    MOVE = 1
    DELETE = 2


class ShapeType(Enum):
    SQUARE = 0
    CIRCLE = 1
    TRIANGLE = 2


class ColorType(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
