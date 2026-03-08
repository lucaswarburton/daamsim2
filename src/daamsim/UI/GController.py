from tkinter import messagebox

from data_classes.CurrentData import CurrentData

from . import DMController
from . import GMUI
from . import Graphs

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
        intruder_speeds = daa_spec.intruder_speed_array
        
        close_vel = data.close_vel
        close_vel_over = data.close_vel_over
        rpa_size = daa_spec.rpas_wingspan
        intruder_detection_threshold = daa_spec.intruder_detection_thresh_arc_min
        intruder_maneuver_delay = daa_spec.intruder_maneuver_delay
        
        if rpas_speed in rpas_speeds and intruder_speed in intruder_speeds:
            exists = False
            if intruder_speed in data.rr_val.keys():
                if rpas_speed in data.rr_val[intruder_speed].keys():
                    exists = True
                    results = [data.rr_val[intruder_speed][rpas_speed], data.points[intruder_speed][rpas_speed]]
                
            if not exists:
                    results = Graphs.PerSpeedPlot.convert_data(azimuthDegOncoming = azimuth_array, \
                        RminOncoming = r_min[intruder_speed][rpas_speed], \
                        azimuthOvertake= azimuth_array, \
                        RminOvertake = r_min_overtake[intruder_speed][rpas_speed], \
                        close_vel = close_vel[intruder_speed][rpas_speed], \
                        close_vel_over = close_vel_over[intruder_speed][rpas_speed],
                        fov = fov,\
                        daa_range = daa_range, \
                        rpa_size = rpa_size, \
                        intruder_detection_threshold = intruder_detection_threshold, \
                        manuever_delay = intruder_maneuver_delay) 
                    if intruder_speed not in data.rr_val.keys():
                        data.rr_val[intruder_speed] = dict()
            
                    if intruder_speed not in data.points.keys():
                        data.points[intruder_speed] = dict()
                    
                    if intruder_speed not in data.srr_val.keys():
                        data.srr_val[intruder_speed] = dict()
                    
                    data.rr_val[intruder_speed][rpas_speed] = results[0]
                    data.points[intruder_speed][rpas_speed] = results[1]
                    data.srr_val[intruder_speed][rpas_speed] = results[2]
                
            rr = results[0]
            points = results[1]
            plt = Graphs.PerSpeedPlot(rpas_speed, intruder_speed, round(rr, 2), daa_range, fov)
            plt.add_points(points)
            Graphs.PerSpeedPlot.show_plt()
        else:
            messagebox.showerror("Invalid RPAS or Intruder speed!")
            
    
    def displayAllPerSpeedGraphs(self):
        res = messagebox.askquestion("Warning","This will generate graphs for all combinations of RPAS speed and Intruder speed. Proceed?")
        res = messagebox.askquestion("Warning","This will generate graphs for all combinations of RPAS speed and Intruder speed. Proceed?")
        if res != "yes":
            return
            
        data: CurrentData = CurrentData()
        r_min = data.r_min_m
        r_min_overtake = data.r_min_over
        close_vel = data.close_vel
        close_vel_over = data.close_vel_over
        daa_spec = data.specs
        fov = daa_spec.daa_fov_deg
        daa_range = daa_spec.daa_declaration_range
        
        rpas_speeds = daa_spec.rpas_speed_array
        rpas_speeds = daa_spec.rpas_speed_array
        intruder_speeds = daa_spec.intruder_speed_array
        azimuth_array = daa_spec.encounter_azimuth_array
        rpa_size = daa_spec.rpas_wingspan
        intruder_detection_threshold = daa_spec.intruder_detection_thresh_arc_min
        intruder_maneuver_delay = daa_spec.intruder_maneuver_delay
        
        
    
        for i, intruder_speed in enumerate(intruder_speeds):
            intruder_speed = round(intruder_speed, 3)
            for rpas_speed in rpas_speeds:
                rpas_speed = round(rpas_speed, 3)
                exists = False
                if intruder_speed in data.rr_val.keys():
                    if rpas_speed in data.rr_val[intruder_speed].keys():
                        exists = True
                        results = [data.rr_val[intruder_speed][rpas_speed], data.points[intruder_speed][rpas_speed]]
                
                if not exists:
                    results = Graphs.PerSpeedPlot.convert_data(azimuthDegOncoming = azimuth_array, \
                        RminOncoming = r_min[intruder_speed][rpas_speed], \
                        azimuthOvertake= azimuth_array, \
                        RminOvertake = r_min_overtake[intruder_speed][rpas_speed], \
                        close_vel = close_vel[intruder_speed][rpas_speed], \
                        close_vel_over = close_vel_over[intruder_speed][rpas_speed],
                        fov = fov,\
                        daa_range = daa_range, \
                        rpa_size = rpa_size, \
                        intruder_detection_threshold = intruder_detection_threshold, \
                        manuever_delay = intruder_maneuver_delay) 
                    if intruder_speed not in data.rr_val.keys():
                        data.rr_val[intruder_speed] = dict()
            
                    if intruder_speed not in data.points.keys():
                        data.points[intruder_speed] = dict()
                    
                    if intruder_speed not in data.srr_val.keys():
                        data.srr_val[intruder_speed] = dict()
                    
                    data.rr_val[intruder_speed][rpas_speed] = results[0]
                    data.points[intruder_speed][rpas_speed] = results[1]
                    data.srr_val[intruder_speed][rpas_speed] = results[2]

                rr = results[0]
                points = results[1]
                plt = Graphs.PerSpeedPlot(rpas_speed, intruder_speed, round(rr, 2), daa_range, fov)
                plt.add_points(points)
        
        Graphs.PerSpeedPlot.show_plt()
        
    def displayRPASSurfaceGraph(self, rpas_speed, down_sample_factor):
        Graphs.RPASSurfaceMultiSpeedPlot(rpas_speed, down_sample_factor)
        
    def displayIntruderSurfaceGraph(self, intruder_speed, down_sample_factor):
        Graphs.IntruderSurfaceMultiSpeedPlot(intruder_speed, down_sample_factor)
        
    def displayRPASLineGraph(self, rpas_speed, down_sample_factor):
        Graphs.RPASLineMultiSpeedPlot(rpas_speed, down_sample_factor)
        
    def displayIntruderLineGraph(self, intruder_speed, down_sample_factor):
        Graphs.IntruderLineMultiSpeedPlot(intruder_speed, down_sample_factor)
        
    def displayNormalizedNoSeeGraph(self, rpas_speed, dist_file_name):
        Graphs.RpasNormalizedRRPassFailNoSee(rpas_speed=rpas_speed, dist_file=dist_file_name)
        
    def displayCumulativeNoSeeGraph(self, rpas_speed, dist_file_name):
        Graphs.RpasCumulativeRRPassFailNoSee(rpas_speed=rpas_speed, dist_file=dist_file_name)
        
    def displayNormalizedSeeAndAvoidGraph(self, rpas_speed, dist_file_name):
        Graphs.RpasNormalizedRRPassFailSeeAndAvoid(rpas_speed=rpas_speed, dist_file=dist_file_name)
    
    def displayCumulativeSeeAndAvoidGraph(self, rpas_speed, dist_file_name):
        Graphs.RpasCumulativeRRPassFailSeeAndAvoid(rpas_speed=rpas_speed, dist_file=dist_file_name)

        

            
            
        