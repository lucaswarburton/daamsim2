from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from daamsim.Config import Configuration
from .SaveLoadController import SaveController

class SaveUI(Frame):
    def __init__(self, controller: SaveController, master, bg = "floral white") -> None:
        super().__init__(master, bg=bg)
        self.controller = controller
        self.bg = bg
        
        self.config:Configuration = Configuration()
        
        self.output_file_path = self.config.default_save_file_path
        print(self.output_file_path)
        
        self.reset()
        
    def select_output_file(self) -> None:
        temp = self.output_file_path.strip().split("/")
        initialdir = self.output_file_path.strip(temp[-1])
        self.output_file_path = filedialog.asksaveasfilename(title="Select output File", initialdir=initialdir, initialfile= temp[-1] if len(temp) > 1 else "", defaultextension=".json", filetypes=[("JSON (*.json)", "*.json")])
        self.reset()
    
    def reset(self) -> None:
        self.title_label = Label(self, text="Save System", font=("Helvetica", 16), background=self.bg)
        self.title_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.output_file_button = Button(self, text="Select output File", command=self.select_output_file)
        self.output_file_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self.output_file_path_entry = Entry(self, textvariable=StringVar(value=self.output_file_path), width=50)
        self.output_file_path_entry.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        
        self.save_file_button = Button(self, text="Save System State", command= lambda: self.controller.save_state(self.output_file_path))
        self.save_file_button.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)


        