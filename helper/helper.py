import numpy as np
import math
import cv2

class Map:
    def __init__(self, width, height, clearance):
        self.width = width
        self.height = height
        self.clearance = clearance
        self.canvas = np.zeros((height, width, 3), dtype='uint8')
        self.horizontal_indices, self.vertical_indices = np.meshgrid(np.arange(self.height), np.arange(self.width), indexing='ij')
        self.clearance_color, self.obstacle_color = [255, 0, 0], [255, 255, 255]
        
    def define_hexagon(self, side):
        height_of_triangle = int((math.sqrt(3)/2) * side)
        
        x1_c, y1_c = int(self.width/2 - height_of_triangle - self.clearance), int(self.height/2 - side/2 - self.clearance/2)
        x2_c, y2_c = int(self.width/2), int(self.height/2 - side - self.clearance)
        x3_c, y3_c = int(self.width/2 - height_of_triangle - self.clearance), int(self.height/2 + side/2 + self.clearance/2)
        x4_c, y4_c = int(self.width/2), int(self.height/2 + side + self.clearance)
        x5_c, y5_c = int(self.width/2 + height_of_triangle + self.clearance), int(self.height/2 + side/2 + self.clearance/2)
        x6_c, y6_c = int(self.width/2 + height_of_triangle + self.clearance), int(self.height/2 - side/2 - self.clearance/2)
        m1_c, m2_c, m3_c, m4_c = (y2_c - y1_c)/ (x2_c - x1_c), (y4_c - y3_c)/(x4_c - x3_c), \
            (y5_c - y4_c)/(x5_c - x4_c), (y6_c - y2_c)/(x6_c - x2_c)
            
        x1, y1 = x1_c + self.clearance, int(y1_c + self.clearance/2)
        x2, y2 = x2_c, int(y2_c + self.clearance)
        x3, y3 = x3_c + self.clearance, int(y3_c - self.clearance/2)
        x4, y4 = x4_c, int(y4_c - self.clearance)
        x5, y5 = x5_c - self.clearance, int(y5_c - self.clearance/2)
        x6, y6 = x6_c - self.clearance, int(y6_c + self.clearance)
        m1, m2, m3, m4 = (y2 - y1)/(x2 - x1), (y4 - y3)/(x4 - x3), \
            (y5 - y4)/ (x5 - x4), (y6 - y2)/(x6 - x2)
        
        for j in range(self.height):
            for i in range(self.width):
                if(
                (i >= (self.width/2 - height_of_triangle - self.clearance)) \
                and (i < self.width/2) \
                and ((j - m1_c * i - y1_c + m1_c * x1_c) >= 0 \
                and (j - m2_c * i - y3_c + m2_c * x3_c) <= 0)
                ):
                    self.canvas[j, i] = self.clearance_color
                         
                if((
                i < (self.width/2 + height_of_triangle + self.clearance)) \
                and (i >= self.width/2) \
                and ((j - m3_c * i - y4_c + m3_c * x4_c) <= 0) \
                and ((j - m4_c * i - y2_c + m4_c * x2_c) >= 0)
                ):
                    self.canvas[j, i] = self.clearance_color
                
                if(
                (i >= (self.width/2 - height_of_triangle)) \
                and (i < self.width/2) \
                and ((j - m1 * i - y1 + m1 * x1) >= 0 \
                and (j - m2 * i - y3 + m2 * x3) <= 0)
                ):
                    self.canvas[j, i] = self.obstacle_color
                    
                if((
                i < (self.width/2 + height_of_triangle )) \
                and (i >= self.width/2) \
                and ((j - m3 * i - y4 + m3 * x4) <= 0) \
                and ((j - m4 * i - y2 + m4 * x2) >= 0)
                ):
                    self.canvas[j, i] = self.obstacle_color
        return
        
    def generate_map(self, side_of_hexagon):
        self.define_hexagon(side_of_hexagon)
        return
    
    def display_map(self):
        map_to_display = self.canvas.copy()
        map_to_display_bgr = cv2.cvtColor(map_to_display, cv2.COLOR_RGB2BGR)
        cv2.imshow("Generated MAP", map_to_display)
        cv2.waitKey(0)
        return
    
    def get_map(self):
        return self.canvas
    
    
if __name__ == "__main__":
    map = Map(600, 250, 5)
    map.generate_map(75)
    map.display_map()