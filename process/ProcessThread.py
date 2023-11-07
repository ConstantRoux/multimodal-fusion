import threading
import time
from interface.DrawingApp import DrawingApp
from process.Command import Command
from slot.EDataType import ActionType
from slot.SlotArray import SlotArray


class ProcessThread(threading.Thread):
    def __init__(self, slotArray: SlotArray, drawingApp: DrawingApp, verbose: bool = False):
        # inheritance
        super(ProcessThread, self).__init__(target=self.callback)
        self._stop_event = threading.Event()

        # args
        self.verbose = verbose
        self.slotArray = slotArray
        self.drawingApp = drawingApp

        # launch thread
        self.start()

        # verbose
        if self.verbose:
            print("[ProcessThread] Thread launched.")

    def callback(self):
        while not self._stop_event.is_set():
            # wait for a new data in the fifo
            data = self.slotArray.fifo.get()

            # verbose
            if self.verbose:
                print("[ProcessThread]", data)

            # update the slot array
            self.slotArray.putArray(data)

            # update the command manager
            self.slotArray.cmd.updateSlotArray(self.slotArray.slotArray)

            # check if it exists a possible command
            state1 = self.slotArray.cmd.checkPossibility()

            # if it exists a possible command
            if state1 == self.slotArray.cmd.POSSIBLE:
                # try to execute the command
                state2 = self.executeCommand(self.slotArray.cmd)
                if state2 == DrawingApp.IMPOSSIBLE:
                    self.slotArray.cmd.clear()
                    self.slotArray.stop("no command found")
                elif state2 == DrawingApp.POSSIBLE:
                    if self.verbose:
                        print("[ProcessThread]", "Too many possibilities.")
                elif state2 == DrawingApp.SAFE:
                    self.slotArray.cmd.clear()
                    self.slotArray.stop("command found")

            # wait to free cpu time
            time.sleep(0.01)

        # verbose
        if self.verbose:
            print("[ProcessThread] Thread killed.")

        # kill tkinter app
        self.drawingApp.root.destroy()

    def stop(self):
        self._stop_event.set()

    def executeCommand(self, cmd: Command) -> int:
        # QUIT
        if cmd.action == ActionType.QUIT:
            self.stop()

        # ADD
        if cmd.action == ActionType.ADD:
            if cmd.color is not None and len(cmd.position) >= 1:
                self.drawingApp.createShape(cmd.shape, colorType=cmd.color, x=cmd.position[0][0], y=cmd.position[0][1])
                self.drawingApp.updateConfidence(cmd.confidence)
                return DrawingApp.SAFE
            else:
                return DrawingApp.POSSIBLE

        # MOVE
        elif cmd.action == ActionType.MOVE:
            if len(cmd.position) == 1:
                outputID = self.drawingApp.getObjectID(shapeType=cmd.shape, colorType=cmd.color)
                if len(outputID) == 0:
                    return DrawingApp.IMPOSSIBLE
                elif len(outputID) == 1:
                    self.drawingApp.moveShape(outputID[0], cmd.position[0][0], cmd.position[0][1])
                    self.drawingApp.updateConfidence(cmd.confidence)
                    return DrawingApp.SAFE
                else:
                    return DrawingApp.POSSIBLE
            elif len(cmd.position) >= 2:
                outputID = self.drawingApp.getObjectID(x=cmd.position[0][0], y=cmd.position[0][1])
                if len(outputID) == 0:
                    return DrawingApp.IMPOSSIBLE
                elif len(outputID) == 1:
                    self.drawingApp.moveShape(outputID[0], cmd.position[1][0], cmd.position[1][1])
                    self.drawingApp.updateConfidence(cmd.confidence)
                    return DrawingApp.SAFE
                else:
                    return DrawingApp.POSSIBLE

        # DELETE
        elif cmd.action == ActionType.DELETE:
            outputID = self.drawingApp.getObjectID(shapeType=cmd.shape, colorType=cmd.color,
                                        x=cmd.position[0][0] if len(cmd.position) > 0 else None,
                                        y=cmd.position[0][1] if len(cmd.position) > 0 else None)
            if len(outputID) == 0:
                return DrawingApp.IMPOSSIBLE
            elif len(outputID) == 1:
                self.drawingApp.deleteShape(outputID[0])
                return DrawingApp.SAFE
            else:
                return DrawingApp.POSSIBLE
