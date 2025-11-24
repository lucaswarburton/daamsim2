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
        azimuthOncoming = data.alpha_oncoming_vect
        azimuthOvertake = data.alpha_overtake_vect
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        daa_spec = data.specs
        if not len(daa_spec) == 0:
            fov = daa_spec.daa_fov_deg
            range = daa_spec.daa_declaration_range
            rtas_speeds = daa_spec.rtas_speed_array
            intruder_speeds = daa_spec.intruder_speed_array
    
            i = 0
            while i < len(azimuthOncoming) and i < len(azimuthOvertake) and i < len(r_min) and i < r_min_overtake:
                results = per_speed_plot.convert_data(azimuthOncoming, r_min, azimuthOvertake, r_min_overtake, fov, range)
                rr = results[0]
                points = results[1]
                cur_rtas_speed = rtas_speeds[int(i/len(rtas_speeds))]
                cur_intruder_speed = intruder_speeds[i%len(intruder_speeds)]
                plt = per_speed_plot(cur_rtas_speed, cur_intruder_speed, rr, range, fov)
                plt.add_points(points)
                plt.show_plt
                i += i
            
        