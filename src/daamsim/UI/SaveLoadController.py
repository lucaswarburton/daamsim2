from data_classes.current_data import CurrentData
from tkinter import messagebox


class SaveController:
    def __init__(self, master_controller):
        self.master_controller = master_controller
        
    def save_state(self, output_file_path) -> bool: 
        try:
            data = CurrentData()
        
            with open(output_file_path, 'w') as f:
                f.write(data.toJSON())
            messagebox.showinfo("Success!", "Data Saved Successfully!")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Unexpected Error Encountered Trying to Save Data")
    
class LoadController:     
    def load_state(input_file_path:str) -> bool:
        data = CurrentData()
        if not input_file_path.endswith(".json"):
            return False
        with open(input_file_path) as f:
            json_string = f.read()
            return data.fromJSON(json_string)