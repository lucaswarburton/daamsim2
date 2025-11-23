from tkinter import *
from tkinter import ttk

from .DMController import DMController
from .window import Window
from .DMUI import DMUIFrame
from .GMUI import GMUIFrame
from .NSUI import new_sim_UI
from .ProgressFrameUI import Progress_Frame
from .NSController import new_sim_controller
from .GController import GraphController

def UI_main():
    w = Window()
    
    main_controller = DMController()
    main_controller.setWindow(w)
    dmui_frame = DMUIFrame(main_controller, master=w)
    main_controller.setView(dmui_frame)
    
    nsim_controller = new_sim_controller(main_controller)
    new_sim_UI_frame = new_sim_UI(nsim_controller, master=w.container)
    nsim_controller.setView(new_sim_UI_frame.scrolling_frame)
    new_sim_UI_frame.grid(row=0, column=0, sticky="nsew")
    w.addFrame("NSUI", new_sim_UI_frame)
    
    g_controller = GraphController(main_controller)
    gmui_frame = GMUIFrame(g_controller, master=w.container)
    gmui_frame.grid(row=0, column=0, sticky="nsew")
    w.addFrame("GMUI", gmui_frame)
    
    progress_frame = Progress_Frame(master = w.container)
    progress_frame.grid(row=0, column=0, sticky="nsew")
    w.addFrame("ProgressFrameUI", progress_frame)

    w.setDMUIFrame(dmui_frame)
    w.setActiveFrame(new_sim_UI_frame)
    
    w.mainloop()


if __name__ == '__main__':
    UI_main()

