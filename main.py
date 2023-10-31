from agent.G2SAgent import G2SAgent
from agent.T2SAgent import T2SAgent
from interface.DrawingApp import DrawingApp
from process.ProcessThread import ProcessThread
from slot.SlotArray import SlotArray
import tkinter as tk


if __name__ == '__main__':
    # create slot array with the queue
    slotArray = SlotArray(5.0, verbose=True)

    # create ivy agents
    t2sAgent = T2SAgent("TextToSlot", slotArray)
    g2sAgent = G2SAgent("GestureToSlot", slotArray)

    # create application interface
    root = tk.Tk()
    app = DrawingApp(root, slotArray)

    # create process thread
    processThread = ProcessThread(slotArray, app, verbose=True)

    # tkinter loop
    root.mainloop()
