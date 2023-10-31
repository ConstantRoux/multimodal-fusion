from slot.Data import Data
from slot.EDataType import ActionType, ShapeType, ColorType


class Command:
    POSSIBLE = 0
    UNKNOWN = -1

    def __init__(self):
        # TODO compute confidence
        # args
        self.slotArray = None

        # vars
        self.action = None
        self.color = None
        self.shape = None
        self.position = []
        self.confidence = 1.0
        self.state = Command.UNKNOWN

    def clear(self):
        self.action = None
        self.color = None
        self.shape = None
        self.position = []
        self.confidence = 1.0
        self.state = Command.UNKNOWN

    def updateSlotArray(self, slotArray: list):
        self.slotArray = slotArray

    def fillParams(self):
        # init params
        self.position = []

        # for each data in the slot array
        for data in self.slotArray:
            # update confidence
            self.confidence *= data.confidence

            # switch between different data types
            # case ACTION
            if data.dataType == data.dataType.ACTION:
                self.action: ActionType = data.value
            # case SHAPE
            elif data.dataType == data.dataType.SHAPE:
                self.shape: ShapeType = data.value
            # case COLOR
            elif data.dataType == data.dataType.COLOR:
                self.color: ColorType = data.value
            # case POSITION
            elif data.dataType == data.dataType.POSITION:
                self.position.append(data.value)

    def checkPossibility(self) -> int:
        # fill params
        self.fillParams()

        # check possibility with the params
        # action ADD
        if self.action is not None and self.action == ActionType.ADD:
            if self.shape is not None:
                self.state = Command.POSSIBLE
                return Command.POSSIBLE
            else:
                self.state = Command.UNKNOWN
                return Command.UNKNOWN

        # action MOVE
        elif self.action is not None and self.action == ActionType.MOVE:
            if (self.shape is not None and len(self.position) >= 1) or len(self.position) >= 2:
                self.state = Command.POSSIBLE
                return Command.POSSIBLE
            else:
                self.state = Command.UNKNOWN
                return Command.UNKNOWN

        # action DELETE
        elif self.action is not None and self.action == ActionType.DELETE:
            if self.shape is not None or len(self.position) >= 1:
                self.state = Command.POSSIBLE
                return Command.POSSIBLE
            else:
                self.state = Command.UNKNOWN
                return Command.UNKNOWN

        # no action found
        else:
            self.state = Command.UNKNOWN
            return Command.UNKNOWN