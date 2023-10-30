from slot.Data import Data
from slot.EDataType import ActionType, ShapeType, ColorType


class Command:
    FOUND = 1
    UNKNOWN = -1

    def __init__(self, slotArray: list):
        # TODO compute confidence
        # args
        self.slotArray = slotArray

        # vars
        self.action = None
        self.color = None
        self.shape = None
        self.position = []
        self.confidence = 0

        # get the command
        self.res = self.findCommand()

    def findCommand(self) -> int:
        # for each data in the slot array
        for i in range(len(self.slotArray)):
            # get data as local variable
            data: Data = self.slotArray[i]

            # switch between different data types
            # case ACTION
            if data.dataType.value == data.dataType.ACTION:
                self.action: ActionType = data.value
            # case SHAPE
            elif data.dataType.value == data.dataType.SHAPE:
                self.shape: ShapeType = data.value
            # case COLOR
            elif data.dataType.value == data.dataType.COLOR:
                self.color: ColorType = data.value
            # case POSITION
            elif data.dataType.value == data.dataType.POSITION:
                self.position.append(data.value)

        # with the current data, try to find a possible command:
        # (P.S.: with a feedback of the interface, it is possible to ask the next iteration to find a better command)
        # action ADD: we need at least the action ADD and a shape (color and position set with default values)
        if self.action is not None and self.action.value == ActionType.ADD:
            if self.shape is not None:
                return Command.FOUND

        # action MOVE: we need at least the action MOVE, a shape and two positions
        if self.action is not None and self.action.value == ActionType.MOVE:
            if self.shape is not None:
                if len(self.position) >= 2:
                    return Command.FOUND

        # action DELETE: we need at least the action DELETE, a shape and one position
        if self.action is not None and self.action.value == ActionType.DELETE:
            if self.shape is not None:
                if len(self.position) >= 1:
                    return Command.FOUND

        # no command found
        return Command.UNKNOWN

    def print(self):
        print(self.action, self.shape, self.color, self.position, self.confidence)
        # TODO
