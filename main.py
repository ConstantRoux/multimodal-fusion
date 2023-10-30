from agent.G2SAgent import G2SAgent
from agent.T2SAgent import T2SAgent
from process.ProcessThread import ProcessThread
from slot.SlotArray import SlotArray

if __name__ == '__main__':
    # create slot array with the queue
    slotArray = SlotArray(5.0, verbose=True)

    # create ivy agents
    t2sAgent = T2SAgent("TextToSlot", slotArray)
    g2sAgent = G2SAgent("GestureToSlot", slotArray)

    # create process thread
    processThread = ProcessThread(slotArray, verbose=True)

    # create application interface
