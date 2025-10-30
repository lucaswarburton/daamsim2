from tkinter import *
from tkinter import ttk

from DMController import DMController
from window import Window
from DMUI import DMUIFrame
from GMUI import GMUIFrame

def main():
    w = Window()
    main_controller = DMController()
    main_controller.setView(w)
    dmui_frame = DMUIFrame(main_controller, master=w)
    gmui_frame = GMUIFrame(main_controller, master=w)

    w.setDMUIFrame(dmui_frame)
    w.setActiveFrame(gmui_frame)

    w.mainloop()


if __name__ == '__main__':
    main()

