from tkinter import *
from tkinter import ttk

from DMController import DMController
from window import Window
from DMUI import DMUIFrame
from GMUI import GMUIFrame
from NSUI import new_sim_UI
from NSController import new_sim_controller

def main():
    w = Window()
    w.container.pack(side = RIGHT, fill="both", expand=True)
    w.container.grid_rowconfigure(0, weight=1)
    w.container.grid_columnconfigure(0, weight=1)
    
    main_controller = DMController()
    main_controller.setView(w)
    dmui_frame = DMUIFrame(main_controller, master=w)
    
    nsim_controller = new_sim_controller(main_controller)
    new_sim_UI_frame = new_sim_UI(nsim_controller, master=w.container)
    nsim_controller.setView(new_sim_UI_frame)
    new_sim_UI_frame.grid(row=0, column=0, sticky="nsew")
    
    w.addFrame("NSUI", new_sim_UI_frame)
    
    gmui_frame = GMUIFrame(main_controller, master=w.container)
    gmui_frame.grid(row=0, column=0, sticky="nsew")
    
    w.addFrame("GMUI", gmui_frame)

    w.setDMUIFrame(dmui_frame)
    w.setActiveFrame(new_sim_UI_frame)
    
    

    w.mainloop()


if __name__ == '__main__':
    main()

