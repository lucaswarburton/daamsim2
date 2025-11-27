from tkinter import messagebox
from .graphs import per_speed_plot
from data_classes.current_data import CurrentData
from daamsim.Config import Configuration

class GraphController:
    def __init__(self, master_controller):
        self.view = None
        self.master_controller = master_controller
        
    def setView(self, view):
        self.view = view
        
    def setActiveFrame(self, frame_name):
        self.view.setActiveFrame(frame_name)
        
    def displayPerSpeedGraph(self, rtas_speed, intruder_speed):
        data = CurrentData()
        
        daa_spec = data.specs
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        azimuth_array = daa_spec.encounter_azimuth_array
        fov = daa_spec.daa_fov_deg
        daa_range = daa_spec.daa_declaration_range
        rtas_speeds = daa_spec.rtas_speed_array
        intruder_speeds = daa_spec.intruder_speed_array
        
        if rtas_speed in rtas_speeds and intruder_speed in intruder_speeds:
            results = per_speed_plot.convert_data(azimuth_array, r_min[intruder_speed][rtas_speed], azimuth_array, r_min_overtake[intruder_speed][rtas_speed], fov, daa_range)
            rr = results[0]
            points = results[1]
            plt = per_speed_plot(rtas_speed, intruder_speed, round(rr, 2), daa_range, fov)
            plt.add_points(points)
            per_speed_plot.show_plt()
        else:
            messagebox.showerror("Invalid RTAS or Intruder speed!")
            
        
        
    
    
    def displayAllPerSpeedGraphs(self):
        res = messagebox.askquestion("Warning","This will generate graphs for all combinations of RTAS speed and Intruder speed. Proceed?")
        if res != "yes":
            return
            
        data = CurrentData()
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        daa_spec = data.specs
        fov = daa_spec.daa_fov_deg
        daa_range = daa_spec.daa_declaration_range
        
        rtas_speeds = daa_spec.rtas_speed_array
        intruder_speeds = daa_spec.intruder_speed_array
        azimuth_array = daa_spec.encounter_azimuth_array
    
        for i, in_speed in enumerate(intruder_speeds):
            in_speed = round(in_speed, 3)
            for rtas_speed in rtas_speeds:
                rtas_speed = round(rtas_speed, 3)
                results = per_speed_plot.convert_data(azimuth_array, r_min[in_speed][rtas_speed], azimuth_array, r_min_overtake[in_speed][rtas_speed], fov, daa_range)
                rr = results[0]
                points = results[1]
                plt = per_speed_plot(rtas_speed, in_speed, round(rr, 2), daa_range, fov)
                plt.add_points(points)
        
        per_speed_plot.show_plt()

            
            
        