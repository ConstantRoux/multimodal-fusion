from ivy.ivy import IvyServer

from slot.Data import Data
from slot.EDataType import ShapeType, DataType
from slot.SlotArray import SlotArray


class G2SAgent(IvyServer):
    def __init__(self, name: str, slotArray: SlotArray):
        # inheritance
        IvyServer.__init__(self, 'G2SAgent')

        # args
        self.name = name
        self.slotArray = slotArray

        # ivy bus
        self.start('127.255.255.255:2010')
        self.bind_msg(self.T2SHandle, '^OneDollarIvy Template=(.*) Confidence=(.*)')

        # keywords
        shape_dict = {ShapeType.RECTANGLE: ["rectangle"],
                      ShapeType.CIRCLE: ["cercle"],
                      ShapeType.TRIANGLE: ["triangle"]}

        self.keywords_dict = {DataType.SHAPE: shape_dict}

    def T2SHandle(self, agent, template: str, confidence: str):
        for key1 in self.keywords_dict:
            for key2 in self.keywords_dict[key1]:
                for word in self.keywords_dict[key1][key2]:
                    if word in template:
                        d = Data(key1, key2, float(confidence.replace(',', '.')))
                        self.slotArray.putFifo(d)
                        self.send_msg(str(d))
