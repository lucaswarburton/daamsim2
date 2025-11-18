from tkinter import *
from tkinter import ttk

class Scroll_Frame(Frame):
    def __init__(self, master, SCROLLFRAMETYPE, controller, bg = None):
        Frame.__init__(self, master, bg=bg)

        self.canvas = Canvas(self, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.scrolling_frame = SCROLLFRAMETYPE(controller = controller, master =self.canvas, bg=bg)
        self.canvas_window = self.canvas.create_window((0,0), window=self.scrolling_frame, anchor = "nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrolling_frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.resize_frame)

    def update_scrollregion(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def resize_frame(self, event=None):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    
    scr_fr = Scroll_Frame(controller=None, master=root, SCROLLFRAMETYPE=Frame)
    scr_fr.pack(fill=BOTH, expand=1)

    for i in range(30):
        lbl = Label(scr_fr.scrolling_frame, text=f"Label {i}")
        lbl.pack()

    root.mainloop()