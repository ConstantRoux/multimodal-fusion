import threading
import time
from interface.DrawingApp import DrawingApp
from slot.SlotArray import SlotArray


class ProcessThread(threading.Thread):
    def __init__(self, slotArray: SlotArray, drawingApp: DrawingApp, confidence_th: float, verbose: bool = False):
        # inheritance
        super(ProcessThread, self).__init__(target=self.callback)
        self._stop_event = threading.Event()

        # args
        self.confidence_th = confidence_th
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

            # continue only if the confidence is high enough
            if data.confidence >= self.confidence_th:
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
                    state2 = self.slotArray.cmd.execute(self.drawingApp)
                    if state2 == DrawingApp.IMPOSSIBLE:
                        self.slotArray.cmd.clear()
                        self.slotArray.stop("no command found")
                    elif state2 == DrawingApp.POSSIBLE:
                        if self.verbose:
                            print("[ProcessThread]", "Too many possibilities.")
                    elif state2 == DrawingApp.SAFE:
                        self.slotArray.cmd.clear()
                        self.slotArray.stop("command found")
                    elif state2 == DrawingApp.QUIT:
                        self.stop()

            # wait to free cpu time
            time.sleep(0.01)

        # verbose
        if self.verbose:
            print("[ProcessThread] Thread killed.")

        # kill tkinter app
        self.drawingApp.root.destroy()

    def stop(self):
        self._stop_event.set()
