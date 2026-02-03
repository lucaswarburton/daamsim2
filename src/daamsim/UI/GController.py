from tkinter import messagebox

from .graphs import PerSpeedPlot
from data_classes.CurrentData import CurrentData

from . import DMController
from . import GMUI

class GraphController:
    def __init__(self, master_controller: DMController.DMController):
        self.view = None
        self.master_controller = master_controller
        
    def set_view(self, view: GMUI.GMUIFrame) -> None:
        self.view = view
        
    def setActiveFrame(self, frame_name) -> None:
        self.view.setActiveFrame(frame_name)
        
    def displayPerSpeedGraph(self, rpas_speed, intruder_speed):
        data = CurrentData()
        
        daa_spec = data.specs
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        azimuth_array = daa_spec.encounter_azimuth_array
        fov = daa_spec.daa_fov_deg
        daa_range = daa_spec.daa_declaration_range
        rpas_speeds = daa_spec.rpas_speed_array
        rpas_speeds = daa_spec.rpas_speed_array
        intruder_speeds = daa_spec.intruder_speed_array
        
        if rpas_speed in rpas_speeds and intruder_speed in intruder_speeds:
            results = PerSpeedPlot.convert_data(azimuth_array, r_min[intruder_speed][rpas_speed], azimuth_array, r_min_overtake[intruder_speed][rpas_speed], fov, daa_range)
            rr = results[0]
            points = results[1]
            plt = PerSpeedPlot(rpas_speed, intruder_speed, round(rr, 2), daa_range, fov)
            plt.add_points(points)
            PerSpeedPlot.show_plt()
        else:
            messagebox.showerror("Invalid RPAS or Intruder speed!")
            messagebox.showerror("Invalid RPAS or Intruder speed!")
            
        
        
    
    
    def displayAllPerSpeedGraphs(self):
        res = messagebox.askquestion("Warning","This will generate graphs for all combinations of RPAS speed and Intruder speed. Proceed?")
        res = messagebox.askquestion("Warning","This will generate graphs for all combinations of RPAS speed and Intruder speed. Proceed?")
        if res != "yes":
            return
            
        data: CurrentData = CurrentData()
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        daa_spec = data.specs
        fov = daa_spec.daa_fov_deg
        daa_range = daa_spec.daa_declaration_range
        
        rpas_speeds = daa_spec.rpas_speed_array
        rpas_speeds = daa_spec.rpas_speed_array
        intruder_speeds = daa_spec.intruder_speed_array
        azimuth_array = daa_spec.encounter_azimuth_array
    
        for i, in_speed in enumerate(intruder_speeds):
            in_speed = round(in_speed, 3)
            for rpas_speed in rpas_speeds:
                rpas_speed = round(rpas_speed, 3)
                results = PerSpeedPlot.convert_data(azimuth_array, r_min[in_speed][rpas_speed], azimuth_array, r_min_overtake[in_speed][rpas_speed], fov, daa_range)
                rr = results[0]
                points = results[1]
                plt = PerSpeedPlot(rpas_speed, in_speed, round(rr, 2), daa_range, fov)
                plt.add_points(points)
        
        PerSpeedPlot.show_plt()

            
            
        