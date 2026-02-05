from calculations.graph_evals import per_speed_graph_evals

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
        return per_speed_graph_evals(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, daa_fov, daa_declaration_range)
            
            
    def show_plt() -> None:
        plt.show()
        
class SurfaceMultiSpeedPlot:
    KTS_TO_MS = 0.514444
    def __init__(self, cmap = "plasma") -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.fig.set_size_inches((7,7))
        self.cmap = cmap
        self.ax.set_xlabel("R min (m)")
        self.ax.set_ylabel("R min (m)")
        # rpas_speed = round(rpas_speed * 0.514444, 1)
        # intruder_speed = round(intruder_speed * 0.514444, 1)  
        # degree_symbol = "\N{DEGREE SIGN}"
        # title = "RPAS Speed: " + str(rpas_speed) + "m/s, Intruder Speed: " + str(intruder_speed) + "m/s, \n FOV = " + str(daa_fov) + degree_symbol + " , Range = " + str(daa_declaration_range) + "m, Risk Ratio = " + str(rr)
        # self.ax.set_title(title)
    
    # def set_title(self, title):
    #     self.ax.set_title(title)
    

    def add_points(self, speeds, multi_speed_points):
        if len(speeds) != len(multi_speed_points):
            raise ValueError("Length of speeds and points ")
        
        Xs = np.array([])
        Ys = np.array([])
        Zs = np.array([])
        i=0
        while i < len(speeds):
            cur_speed = speeds[i]
            points = multi_speed_points[i]
            Xs.append(points[1] * np.cos(points[0]))
            Ys.append(points[1] * np.sin(points[0]))
            Zs.append(np.full(len(points[1]), cur_speed))
        
        surf = self.ax.plot_surface(Xs, Ys, Zs, cmap = self.cmap)
        self.fig.colorbar(surf)
        
    
class LineMultiSpeedPlot:
    KTS_TO_MS = 0.514444
    def __init__(self) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.fig.set_size_inches((7,7))

        # rpas_speed = round(rpas_speed * 0.514444, 1)
        # intruder_speed = round(intruder_speed * 0.514444, 1)  
        # degree_symbol = "\N{DEGREE SIGN}"
        # title = "RPAS Speed: " + str(rpas_speed) + "m/s, Intruder Speed: " + str(intruder_speed) + "m/s, \n FOV = " + str(daa_fov) + degree_symbol + " , Range = " + str(daa_declaration_range) + "m, Risk Ratio = " + str(rr)
        # self.ax.set_title(title)
        
    # def set_title(self, title):
    #     self.ax.set_title(title)
        
    # def set_zlabel(self, zlabel):
    #     self.ax.set_xlabel(zlabel)
        
    def add_points(self, speeds, multi_speed_points):
        if len(speeds) != len(multi_speed_points):
            raise ValueError("Length of speeds and points ")
        
        i=0
        while i < len(speeds):
            cur_speed = speeds[i]
            points = multi_speed_points[i]
            
            pass_x_array = []
            pass_y_array = []
            pass_z_array = []
            
            fail_x_array = []
            fail_y_array = []
            fail_z_array = []
            
            j=0
            while j < len(points[2]):
                if points[2][j] == PASS_COLOUR:
                    pass_x_array.append(points[1][j] * np.cos(points[0][j]))
                    pass_y_array.append(points[1][j] * np.sin(points[0][j]))
                    pass_z_array.append(cur_speed)
                    
                else:
                    fail_x_array.append(points[1][j] * np.cos(points[0][j]))
                    fail_y_array.append(points[1][j] * np.sin(points[0][j]))
                    fail_z_array.append(cur_speed)
                j += 1
            
            
        
        self.ax.plot3D(pass_x_array, pass_y_array, pass_z_array, PASS_COLOUR)
        self.ax.plot3D(fail_x_array, fail_y_array, fail_z_array, FAIL_COLOUR)
  
        
        
            
if __name__ == "__main__":
    plot1 = PerSpeedPlot(10, 10, 0.25, 1000, 60)
    azimuth = np.array([-90*np.pi/180, 10*np.pi/180, 90*np.pi/180])
    rmin = np.array([500,300,400])
    colour = np.array(["red", "green", "red"])
    points = (azimuth, rmin, colour)
    plot1.add_points(points)
    PerSpeedPlot.show_plt()
    