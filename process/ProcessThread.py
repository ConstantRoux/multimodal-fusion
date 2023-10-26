import threading
import time


class ProcessThread(threading.Thread):
    def __init__(self, verbose: bool = False):
        # inheritance
        super(ProcessThread, self).__init__(target=self.callback)

        # get args
        self.verbose = verbose

        # variables

        # launch thread
        self.start()

        # verbose
        if self.verbose:
            print("Thread Process launched")

    def callback(self):
        while True:
            # wait to free cpu time
            time.sleep(0.01)
