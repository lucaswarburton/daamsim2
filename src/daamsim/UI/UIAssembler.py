from tkinter import *
from tkinter import ttk

from .DMController import DMController
from .Window import Window
from .DMUI import DMUIFrame
from .GMUI import GMUIFrame
from .NSUI import NewSimUI
from .SaveLoadUI import SaveUI
from .ProgressFrameUI import ProgressFrame
from .NSController import NewSimController
from .GController import GraphController
from .SaveLoadController import SaveController

def UI_main() -> None:
    w = Window()
    
    main_controller = DMController()
    main_controller.set_window(w)
    dmui_frame = DMUIFrame(main_controller, master=w)
    main_controller.set_view(dmui_frame)
    
    nsim_controller = NewSimController(main_controller)
    new_sim_UI_frame = NewSimUI(nsim_controller, master=w.container)
    nsim_controller.set_view(new_sim_UI_frame.scrolling_frame)
    new_sim_UI_frame.grid(row=0, column=0, sticky="nsew")
    w.add_frame("NSUI", new_sim_UI_frame)
    
    g_controller = GraphController(main_controller)
    gmui_frame = GMUIFrame(g_controller, master=w.container)
    g_controller.set_view(gmui_frame)
    gmui_frame.grid(row=0, column=0, sticky="nsew")
    w.add_frame("GMUI", gmui_frame)
    
    progress_frame = ProgressFrame(master = w.container)
    progress_frame.grid(row=0, column=0, sticky="nsew")
    w.add_frame("ProgressFrameUI", progress_frame)
    
    save_controller = SaveController(main_controller, new_sim_UI_frame.scrolling_frame)
    save_frame = SaveUI(save_controller, master = w.container)
    save_frame.grid(row=0, column=0, sticky="nsew")
    w.add_frame("SAVE", save_frame)

    w.set_DMUI_frame(dmui_frame)
    w.set_active_frame(new_sim_UI_frame)
    
    w.mainloop()


if __name__ == '__main__':
    UI_main()

