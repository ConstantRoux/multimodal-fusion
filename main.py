from acquisition.AcquisitionThread import AcquisitionThread
from slot.SlotArray import SlotArray

if __name__ == '__main__':
    # create slot array with the queue
    slotArray = SlotArray()

    # create acquisition thread
    acquisitionThread = AcquisitionThread(slotArray, 5.0, verbose=True)

    # create process thread
    # create application interface
