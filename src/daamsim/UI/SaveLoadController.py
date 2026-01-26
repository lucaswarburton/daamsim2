from tkinter import messagebox

from data_classes.CurrentData import CurrentData
from . import NSUI
from . import DMController

class SaveController:
    def __init__(self, master_controller, nsui) -> None:
        self.master_controller: DMController.DMController = master_controller
        self.nsui: NSUI.NewSimUIInnerFrame = nsui
        
    def save_state(self, output_file_path:str) -> bool: 
        try:
            data: CurrentData = CurrentData()
            
            #Only save current params if we do not have an existing data set
            if data._sim_state == 0:
                data.specs = self.nsui.get_params()
                self.nsui.save_current_settings()
        
            with open(output_file_path, 'w') as f:
                f.write(data.to_json())
            messagebox.showinfo("Success!", "Data Saved Successfully!")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unexpected Error Encountered Trying to Save Data")
    
class LoadController:     
    def load_state(input_file_path:str) -> bool:
        
        data:CurrentData = CurrentData()
        if not input_file_path.endswith(".json"):
            return False
        with open(input_file_path) as f:
            json_string = f.read()
            return data.from_json(json_string)
        