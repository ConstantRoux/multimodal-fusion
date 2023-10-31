from ivy.ivy import IvyServer
from slot.Data import Data
from slot.EDataType import DataType, ActionType, ShapeType, ColorType
from slot.SlotArray import SlotArray


class T2SAgent(IvyServer):
    def __init__(self, name: str, slotArray: SlotArray):
        # inheritance
        IvyServer.__init__(self, 'T2SAgent')

        # args
        self.name = name
        self.slotArray = slotArray

        # ivy bus
        self.start('127.255.255.255:2010')
        self.bind_msg(self.T2SHandle, '^sra5 Text=(.*) Confidence=(.*)')

        # keywords
        # TODO implement other kind of types
        action_dict = {ActionType.ADD: ["creer", "dessiner", "tracer"],
                       ActionType.MOVE: ["deplacer", "bouger"],
                       ActionType.DELETE: ["supprimer", "effacer"]}

        shape_dict = {ShapeType.RECTANGLE: ["rectangle"],
                      ShapeType.CIRCLE: ["cercle"],
                      ShapeType.TRIANGLE: ["triangle"]}

        color_dict = {ColorType.RED: ["rouge"],
                      ColorType.GREEN: ["vert"],
                      ColorType.BLUE: ["bleu"]}

        self.keywords_dict = {DataType.ACTION: action_dict,
                              DataType.SHAPE: shape_dict,
                              DataType.COLOR: color_dict}

    def T2SHandle(self, agent, text: str, confidence: str):
        for key1 in self.keywords_dict:
            for key2 in self.keywords_dict[key1]:
                for word in self.keywords_dict[key1][key2]:
                    if word in text:
                        d = Data(key1, key2, float(confidence.replace(',', '.')))
                        self.slotArray.putFifo(d)
                        self.send_msg(str(d))
