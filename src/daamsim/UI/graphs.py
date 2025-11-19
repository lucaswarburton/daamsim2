import matplotlib.pyplot as plt 
import numpy as np

class per_speed_plot:
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

        # Plot the radial line
        ax.plot(np.full_like(radii, right_angle), radii, color='black', linestyle='-', label='FOV Right')
        ax.plot(np.full_like(radii, left_angle), radii, color='black', linestyle='-', label='FOV Left')
        ax.plot(left_curve, np.full_like(left_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Left')
        ax.plot(right_curve, np.full_like(right_curve, daa_declaration_range), color='black', linestyle='-', label='FOV Curve Right')
        ax.plot(1000, 30 * np.pi/180)
        plt.show()
        
        
    #Placeholder function var names  
    def add_point(self, distance, azimuth, isCollision):
        if isCollision:
            colour = "red"
        else:
            colour = "green"
        self.ax.scatter(distance, azimuth, c=colour)
    
    #placeholder function var names
    def add_points(self, points):
        for point in points:
            distance = point[0]
            azimuth = point[1]
            isCollision = point[2]
            self.add_point(distance=distance, azimuth=azimuth, isCollision=isCollision)
            
if __name__ == "__main__":
    per_speed_plot(10, 10, 0.25, 1000, 60)