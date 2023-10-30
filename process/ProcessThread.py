import threading
import time

from process.Command import Command
from slot.SlotArray import SlotArray


class ProcessThread(threading.Thread):
    def __init__(self, slotArray: SlotArray, verbose: bool = False):
        # inheritance
        super(ProcessThread, self).__init__(target=self.callback)

        # args
        self.verbose = verbose
        self.slotArray = slotArray

        # launch thread
        self.start()

        # verbose
        if self.verbose:
            print("Thread Process launched")

    def callback(self):
        while True:
            # wait for a new data in the fifo
            data = self.slotArray.fifo.get()

            # verbose
            if self.verbose:
                print(data)

            # update the slot array
            self.slotArray.putArray(data)

            # compute a command
            cmd = Command(self.slotArray.slotArray)

            # switch case
            if cmd.res == Command.FOUND:
                self.slotArray.clear()
                cmd.print()
                # TODO send the command to the interface

            # wait to free cpu time
            time.sleep(0.01)
