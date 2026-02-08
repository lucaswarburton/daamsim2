import matplotlib.pyplot as plt 
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from  calculations import graph_evals 
from data_classes.CurrentData import CurrentData

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
    def __init__(self, down_sample_factor = 1) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.fig.set_size_inches((7,7))
        self.ax.set_xlabel("R min (m)")
        self.ax.set_ylabel("R min (m)")
        self.down_sample_factor = down_sample_factor

        
    #Note: This section could be improved to reduce holes in the line. The issue is that there are non-continuous sections in how the data is calculated in graph_evals
    def add_points(self, speeds, multi_speed_points):
        if len(speeds) != len(multi_speed_points):
            raise ValueError("Length of speeds and points ")
        
        i=0
        keys = list(multi_speed_points.keys())
        while i < len(speeds):
            cur_speed = speeds[i]
            points = multi_speed_points[cur_speed]
            
            lines = []
            colours = []
            
            lengths = []
            
            j=0
            
            #Plot set of lines
            #Note: This section is done due to the fact the dataset is not continuous and we are trying to keep performance when rendering the graph
            
            while j < len(points[2]):
                #Green lines for passing points
                if points[2][j] == PASS_COLOUR and points[2][j-1] == PASS_COLOUR:
                    x2 =  points[1][j] * np.cos(points[0][j])
                    y2 = points[1][j] * np.sin(points[0][j])
                    z2 =  cur_speed
                    
                    x1 =  points[1][j-1] * np.cos(points[0][j-1])
                    y1 = points[1][j-1] * np.sin(points[0][j-1])
                    z1 =  cur_speed
                    
                    lines.append([tuple([x1, y1, z1]), tuple([x2, y2, z2])])
                    colours.append(PASS_COLOUR)
                    
                    length = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
                    
                    lengths.append(length)
                
                #Red lines otherwise
                else:
                    x2 =  points[1][j] * np.cos(points[0][j])
                    y2 = points[1][j] * np.sin(points[0][j])
                    z2 =  cur_speed
                    
                    x1 =  points[1][j-1] * np.cos(points[0][j-1])
                    y1 = points[1][j-1] * np.sin(points[0][j-1])
                    z1 =  cur_speed
                    
                    lines.append([tuple([x1, y1, z1]), tuple([x2, y2, z2])])
                    colours.append(FAIL_COLOUR)
                    
                    length = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
                    
                    lengths.append(length)
                j += self.down_sample_factor
                
            #Now we eleminate extreme outlier lines     
            #Note: We can use Line3DCollection and add_collection3D to plot these individual lines, but this causes performance issues. Instead let's plot continuous segments    
            mean = np.mean(lengths)
            std = np.std(lengths)
            
            NUM_STANDARD_DEVIATIONS_TO_OUTLIER = 3
            
            
            j = 0
            start = 0
            current_colour = colours[0]
            #Iterate through individual line segments
            while j < len(lines):
                #If this line needs to end because the next segment is too long or is a different colour
                if (j < len(lines) and (lengths[j] > (mean + (std * NUM_STANDARD_DEVIATIONS_TO_OUTLIER)))):
                    Xs = []
                    Ys = []
                    Zs = []
                    
                    k = start
                    #Add x1 y1 z1 for each line segment to Xs, Ys, Zs
                    while k <= j:
                        Xs.append(lines[k][0][0])
                        Ys.append(lines[k][0][1])
                        Zs.append(lines[k][0][2])
                        k += 1
                    
                    #Plot this line for Xs, Ys, Zs with curren_colour for the line colour
                    self.ax.plot3D(Xs, Ys, Zs, current_colour)
                    
                    #Because this line segment is an outlier, we want to start after this segment
                    if j + 1 < len(lines):
                        start = j + 1
                        current_colour = (colours[j+1])
                    
                elif current_colour != colours[j]:
                    Xs = []
                    Ys = []
                    Zs = []
                    
                    k = start
                    #Add x1 y1 z1 for each line segment to Xs, Ys, Zs
                    while k <= j:
                        Xs.append(lines[k][0][0])
                        Ys.append(lines[k][0][1])
                        Zs.append(lines[k][0][2])
                        k += 1
                    
                    #Plot this line for Xs, Ys, Zs with curren_colour for the line colour
                    self.ax.plot3D(Xs, Ys, Zs, current_colour)
                    
                    #We can start at this segment because it is just a change in colour
                    start = j
                    current_colour = (colours[j])
                    
                j += 1
            
            Xs = []
            Ys = []
            Zs = []
                    
            k = start
            #Add x1 y1 z1 for each line segment to Xs, Ys, Zs
            while k < j:
                Xs.append(lines[k][0][0])
                Ys.append(lines[k][0][1])
                Zs.append(lines[k][0][2])
                k += 1
            
            self.ax.plot3D(Xs, Ys, Zs, current_colour)
            
                
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
    def __init__(self, intruder_speed, down_sample_factor = 1):
        super().__init__(down_sample_factor= down_sample_factor)
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
    def __init__(self, rpas_speed, down_sample_factor = 1):
        super().__init__(down_sample_factor= down_sample_factor)
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
            
# if __name__ == "__main__":
#     plot1 = PerSpeedPlot(10, 10, 0.25, 1000, 60)
#     azimuth = np.array([-90*np.pi/180, 10*np.pi/180, 90*np.pi/180])
#     rmin = np.array([500,300,400])
#     colour = np.array(["red", "green", "red"])
#     points = (azimuth, rmin, colour)
#     plot1.add_points(points)
#     PerSpeedPlot.show_plt()
    
