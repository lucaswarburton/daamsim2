from  calculations import graph_evals 
from data_classes.CurrentData import CurrentData

import matplotlib.pyplot as plt 
import numpy as np
import math

FAIL_COLOUR = "red"
PASS_COLOUR = "green"

class PerSpeedPlot:
    KTS_TO_MS = 0.514444
    def __init__(self, rpas_speed, intruder_speed, rr, daa_declaration_range, daa_fov) -> None:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        fig.set_size_inches((7,7))
        self.ax = ax
        self.ax.set_theta_zero_location("N")#Orient upwards
        self.ax.set_theta_direction(-1)#Clockwise deg
        right_angle = np.deg2rad(daa_fov/2)
        left_angle = 2 * np.pi - np.deg2rad(daa_fov/2)
        left_curve = np.linspace(left_angle, 2*np.pi, 100)
        right_curve = np.linspace(0, right_angle, 100)
        radii = np.linspace(0, daa_declaration_range, 100) # From r=0 to r=5
        
        rpas_speed = round(rpas_speed * 0.514444, 1)
        intruder_speed = round(intruder_speed * 0.514444, 1)
        

        # Plot the radial line
        ax.plot(np.full_like(radii, right_angle), radii, color='black', linestyle='-', label='FOV Right')
        ax.plot(np.full_like(radii, left_angle), radii, color='black', linestyle='-', label='FOV Left')
        ax.plot(left_curve, np.full_like(left_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Left')
        ax.plot(right_curve, np.full_like(right_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Right')
        ax.plot(1000, 30 * np.pi/180)
        degree_symbol = "\N{DEGREE SIGN}"
        title = "RPAS Speed: " + str(rpas_speed) + "m/s, Intruder Speed: " + str(intruder_speed) + "m/s, \n FOV = " + str(daa_fov) + degree_symbol + " , Range = " + str(daa_declaration_range) + "m, Risk Ratio = " + str(rr)
        ax.set_title(title)
        
        
    def add_point(self, distance, azimuth, isCollision) -> None:
        if isCollision:
            colour = "red"
        else:
            colour = "green"
        self.ax.scatter(distance, azimuth, c=colour)
    
    def add_points(self, points) -> None:
        self.ax.scatter(points[0], points[1], c=points[2])
            
    def convert_data(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, daa_fov, daa_declaration_range) -> list:
        return graph_evals.per_speed_graph_evals(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, daa_fov, daa_declaration_range)
            
            
    def show_plt() -> None:
        plt.show()
        
class SurfaceMultiSpeedPlot:
    KTS_TO_MS = 0.514444
    def __init__(self, cmap = "plasma", down_sample_factor = 1) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.fig.set_size_inches((7,7))
        self.cmap = cmap
        self.ax.set_xlabel("R min (m)")
        self.ax.set_ylabel("R min (m)")
 
        self.down_sample_factor = down_sample_factor
    
    # def set_title(self, title):
    #     self.ax.set_title(title)
    

    def add_points(self, speeds, multi_speed_points):
        if len(speeds) != len(multi_speed_points):
            raise ValueError("Length of speeds and points ")
        
        Xs = np.array([])
        Ys = np.array([])
        Zs = np.array([])
        
        i=0
        keys = list(multi_speed_points.keys())
        while i < len(speeds):
            cur_speed = speeds[i]
            points = multi_speed_points[speeds[i]]
            x = points[1] * np.cos(points[0])
            Xs = np.append(Xs, x)
            y = points[1] * np.sin(points[0])
            Ys= np.append(Ys, y)
            z = np.full(len(points[1]), cur_speed)
            Zs = np.append(Zs, z)
            i += 1
        
        surf = self.ax.plot_trisurf(Xs[::self.down_sample_factor], Ys[::self.down_sample_factor], Zs[::self.down_sample_factor], linewidth=0, antialiased=False, cmap = self.cmap)
        self.fig.colorbar(surf)
        
    
class LineMultiSpeedPlot:
    KTS_TO_MS = 0.514444
    def __init__(self) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.fig.set_size_inches((7,7))
        self.ax.set_xlabel("R min (m)")
        self.ax.set_ylabel("R min (m)")

        
    def add_points(self, speeds, multi_speed_points):
        if len(speeds) != len(multi_speed_points):
            raise ValueError("Length of speeds and points ")
        
        i=0
        keys = list(multi_speed_points.keys())
        while i < len(speeds):
            cur_speed = speeds[i]
            points = multi_speed_points[cur_speed]
            
            pass_x_array = np.array([])
            pass_y_array = np.array([])
            pass_z_array = np.array([])
            
            fail_x_array = np.array([])
            fail_y_array = np.array([])
            fail_z_array = np.array([])
            
            j=0
            while j < len(points[2]):
                if points[2][j] == PASS_COLOUR:
                    pass_x_array = np.append(pass_x_array, points[1][j] * np.cos(points[0][j]))
                    pass_y_array = np.append(pass_y_array, points[1][j] * np.sin(points[0][j]))
                    pass_z_array = np.append(pass_z_array, cur_speed)
                    
                else:
                    fail_x_array = np.append(fail_x_array, points[1][j] * np.cos(points[0][j]))
                    fail_y_array = np.append(fail_y_array, points[1][j] * np.sin(points[0][j]))
                    fail_z_array = np.append(fail_z_array, cur_speed)
                j += 1
    
            
            self.ax.plot3D(pass_x_array, pass_y_array, pass_z_array, PASS_COLOUR)
            self.ax.plot3D(fail_x_array, fail_y_array, fail_z_array, FAIL_COLOUR)
            i += 1
            
        
        
  
class IntruderSurfaceMultiSpeedPlot(SurfaceMultiSpeedPlot):
    def __init__(self, intruder_speed, down_sample_factor = 1):
        super().__init__(down_sample_factor=down_sample_factor)
        self.intruder_speed = intruder_speed
        self.data = CurrentData()
        degree_symbol = "\N{DEGREE SIGN}"
        title = "R min 3D Plot with Intruder Speed: " + str(intruder_speed) + "kts, Bank Angle: " + str(self.data.specs.rpas_max_bank_deg) + degree_symbol +"m/s, \n FOV = " + str(self.data.specs.daa_fov_deg) + degree_symbol + " , Range = " + str(self.data.specs.daa_declaration_range) + "m, and various RPAS Speeds."
        self.ax.set_title(title)
        self.ax.set_zlabel("RPAS speed (kts)")
        graph_evals.calculate_rr_points_for_intruder_speed(intruder_speed)
        
        points = self.assemble_points()
        self.add_points(self.data.specs.rpas_speed_array, points)
        
        plt.show()
        
    def assemble_points(self):
        all_points = self.data.points
        return all_points[self.intruder_speed]
    
    
class RPASSurfaceMultiSpeedPlot(SurfaceMultiSpeedPlot):
    def __init__(self, rpas_speed, down_sample_factor = 1):
        super().__init__(down_sample_factor=down_sample_factor)
        self.rpas_speed = rpas_speed
        self.data = CurrentData()
        degree_symbol = "\N{DEGREE SIGN}"
        title = "R min 3D Plot with RPAS Speed: " + str(rpas_speed) + "kts, Bank Angle: " + str(self.data.specs.rpas_max_bank_deg) + degree_symbol +"m/s, \n FOV = " + str(self.data.specs.daa_fov_deg) + degree_symbol + " , Range = " + str(self.data.specs.daa_declaration_range) + "m, and various Intruder Speeds."
        self.ax.set_title(title)
        self.ax.set_zlabel("Intruder speed (kts)")
        graph_evals.calculate_rr_points_for_rpas_speed(rpas_speed)
        
        points = self.assemble_points()
        self.add_points(self.data.specs.intruder_speed_array, points)
        
        plt.show()
        
    def assemble_points(self):
        all_points = self.data.points
        points = dict()
        for key in all_points.keys():
            points[key] = all_points[key][self.rpas_speed]
        return points

class IntruderLineMultiSpeedPlot(LineMultiSpeedPlot):
    def __init__(self, intruder_speed):
        super().__init__()
        self.intruder_speed = intruder_speed
        self.data = CurrentData()
        degree_symbol = "\N{DEGREE SIGN}"
        title = "R min 3D Plot with Intruder Speed: " + str(intruder_speed) + "kts, Bank Angle: " + str(self.data.specs.rpas_max_bank_deg) + degree_symbol +"m/s, \n FOV = " + str(self.data.specs.daa_fov_deg) + degree_symbol + " , Range = " + str(self.data.specs.daa_declaration_range) + "m, and various RPAS Speeds. (No See)"
        self.ax.set_title(title)
        self.ax.set_zlabel("RPAS speed (kts)")
        graph_evals.calculate_rr_points_for_intruder_speed(intruder_speed)
        
        points = self.assemble_points()
        self.add_points(self.data.specs.rpas_speed_array, points)
        
        plt.show()
        
    def assemble_points(self):
        all_points = self.data.points
        return all_points[self.intruder_speed]
    
    
class RPASLineMultiSpeedPlot(LineMultiSpeedPlot):
    def __init__(self, rpas_speed):
        super().__init__()
        self.rpas_speed = rpas_speed
        self.data = CurrentData()
        degree_symbol = "\N{DEGREE SIGN}"
        title = "R min 3D Plot with RPAS Speed: " + str(rpas_speed) + "kts, Bank Angle: " + str(self.data.specs.rpas_max_bank_deg) + degree_symbol +"m/s, \n FOV = " + str(self.data.specs.daa_fov_deg) + degree_symbol + " , Range = " + str(self.data.specs.daa_declaration_range) + "m, and various Intruder Speeds. (No See)"
        self.ax.set_title(title)
        self.ax.set_zlabel("Intruder speed (kts)")
        graph_evals.calculate_rr_points_for_rpas_speed(rpas_speed)
        
        points = self.assemble_points()
        self.add_points(self.data.specs.intruder_speed_array, points)
        
        plt.show()
        
    def assemble_points(self):
        all_points = self.data.points
        points = dict()
        for key in all_points.keys():
            points[key] = all_points[key][self.rpas_speed]
        return points        
            
if __name__ == "__main__":
    plot1 = PerSpeedPlot(10, 10, 0.25, 1000, 60)
    azimuth = np.array([-90*np.pi/180, 10*np.pi/180, 90*np.pi/180])
    rmin = np.array([500,300,400])
    colour = np.array(["red", "green", "red"])
    points = (azimuth, rmin, colour)
    plot1.add_points(points)
    PerSpeedPlot.show_plt()
    