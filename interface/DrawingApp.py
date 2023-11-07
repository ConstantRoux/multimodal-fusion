import tkinter
import tkinter as tk
import numpy as np
from interface.Object import Object
from process.Command import Command
from slot.Data import Data
from slot.EDataType import ShapeType, ColorType, DataType, ActionType
from slot.SlotArray import SlotArray


class DrawingApp:
    IMPOSSIBLE = -1
    POSSIBLE = 0
    SAFE = 2

    def __init__(self, root: tkinter.Tk, slotArray: SlotArray, width: int = 800, height: int = 800, size: int = 50):
        # args
        self.root = root
        self.slotArray = slotArray
        self.width = width
        self.height = height
        self.size = size

        # vars
        self.tk_color = {ColorType.RED: "red",
                         ColorType.GREEN: "green",
                         ColorType.BLUE: "blue"}

        # interface
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()
        self.label = tk.Label(root, text="Confidence: 0.0")
        self.label.pack(anchor="se", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.leftClickHandle)

        # objects on the canvas
        self.objects = {}

    def updateConfidence(self, confidence):
        self.label.config(text=f"Confidence: {confidence:.2f}")

    def leftClickHandle(self, event):
        x, y = event.x, event.y
        d = Data(DataType.POSITION, (x, y), 1)
        self.slotArray.putFifo(d)

    def createShape(self, shapeType: ShapeType, colorType: ColorType, x: int, y: int):
        if shapeType == ShapeType.RECTANGLE:
            objectID = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=self.tk_color[colorType])
        elif shapeType == ShapeType.CIRCLE:
            objectID = self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=self.tk_color[colorType])
        elif shapeType == ShapeType.TRIANGLE:
            objectID = self.canvas.create_polygon(x, y, x + int(self.size / 2), y + self.size, x + self.size, y,
                                                  fill=self.tk_color[colorType])
        else:
            return
        self.objects[objectID] = Object(objectID, shapeType, colorType, x, y, self.size)

    def deleteShape(self, objectID: int):
        if objectID in self.objects:
            self.canvas.delete(objectID)
            del self.objects[objectID]

    def moveShape(self, objectID: int, x: int, y: int):
        if objectID in self.objects:
            current_x, current_y = self.objects[objectID].x, self.objects[objectID].y
            dx = x - current_x
            dy = y - current_y
            self.objects[objectID].x = x
            self.objects[objectID].y = y
            self.canvas.move(objectID, dx, dy)

    def getObjectID(self, shapeType: ShapeType = None, colorType: ColorType = None, x: int = None,
                    y: int = None) -> list:
        outputID = []

        for objectID in self.objects:
            # case 1: shape
            if shapeType is not None and colorType is None and x is None and y is None:
                if shapeType == self.objects[objectID].shapeType:
                    outputID.append(objectID)

            # case 2: shape and pos
            elif shapeType is not None and colorType is None and x is not None and y is not None:
                if shapeType == self.objects[objectID].shapeType and np.linalg.norm(
                        np.array([x, y]) - np.array([self.objects[objectID].x, self.objects[objectID].y])) <= self.size:
                    outputID.append(objectID)

            # case 3: shape and color
            elif shapeType is not None and colorType is not None and x is None and y is None:
                if shapeType == self.objects[objectID].shapeType and colorType == self.objects[objectID].colorType:
                    outputID.append(objectID)

            # case 4: shape, color and pos
            elif shapeType is not None and colorType is not None and x is not None and y is not None:
                if shapeType == self.objects[objectID].shapeType and colorType == self.objects[
                    objectID].colorType and np.linalg.norm(
                        np.array([x, y]) - np.array([self.objects[objectID].x, self.objects[objectID].y])) <= self.size:
                    outputID.append(objectID)

            # case 5: pos
            elif shapeType is None and colorType is None and x is not None and y is not None:
                if np.linalg.norm(
                        np.array([x, y]) - np.array([self.objects[objectID].x, self.objects[objectID].y])) <= self.size:
                    outputID.append(objectID)

        return outputID
