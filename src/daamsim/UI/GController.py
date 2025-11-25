from .graphs import per_speed_plot
from data_classes.current_data import CurrentData
from daamsim.Config import Configuration

class GraphController:
    def __init__(self, master_controller):
        self.model = None
        self.view = None
        self.master_controller = master_controller
    
    def setmodel(self, model):
        self.model =  model
        
    def setView(self, view):
        self.view = view
    
    def displayAllGraphs(self):
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

            
            
        