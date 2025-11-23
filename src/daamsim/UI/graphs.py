import matplotlib.pyplot as plt 
import numpy as np
from calculations.graph_evals import per_speed_graph_evals

class per_speed_plot:
    KTS_TO_MS = 0.514444
    def __init__(self, rtas_speed, intruder_speed, rr, daa_declaration_range, daa_fov):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.ax = ax
        self.ax.set_theta_zero_location("N")#Orient upwards
        self.ax.set_theta_direction(-1)#Clockwise deg
        right_angle = np.deg2rad(daa_fov/2)
        left_angle = 2 * np.pi - np.deg2rad(daa_fov/2)
        left_curve = np.linspace(left_angle, 2*np.pi, 100)
        right_curve = np.linspace(0, right_angle, 100)
        radii = np.linspace(0, daa_declaration_range, 100) # From r=0 to r=5
        
        rtas_speed = round(rtas_speed * 0.514444, 1)
        intruder_speed = round(intruder_speed * 0.514444, 1)
        

        # Plot the radial line
        ax.plot(np.full_like(radii, right_angle), radii, color='black', linestyle='-', label='FOV Right')
        ax.plot(np.full_like(radii, left_angle), radii, color='black', linestyle='-', label='FOV Left')
        ax.plot(left_curve, np.full_like(left_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Left')
        ax.plot(right_curve, np.full_like(right_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Right')
        ax.plot(1000, 30 * np.pi/180)
        degree_symbol = "\N{DEGREE SIGN}"
        title = "RTAS Speed: " + str(rtas_speed) + "m/s, Intruder Speed: " + str(intruder_speed) + "m/s, \n FOV = " + str(daa_fov) + degree_symbol + " , Range = " + str(daa_declaration_range) + "m, Risk Ratio = " + str(rr)
        ax.set_title(title)
        
    #Placeholder function var names  
    def add_point(self, distance, azimuth, isCollision):
        if isCollision:
            colour = "red"
        else:
            colour = "green"
        self.ax.scatter(distance, azimuth, c=colour)
    
    #placeholder function var names
    def add_points(self, points):
        self.ax.scatter(points[0], points[1], c=points[2])
            
    def convert_data(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, daa_fov, daa_declaration_range):
        return per_speed_graph_evals(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, daa_fov, daa_declaration_range)
            
            
    def show_plt(self):
        plt.show()
            
if __name__ == "__main__":
    plot1 = per_speed_plot(10, 10, 0.25, 1000, 60)
    plot1.show_plt()
    