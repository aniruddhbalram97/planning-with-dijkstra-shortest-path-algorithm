import numpy as np
import math
import cv2
from queue import PriorityQueue

class Map:
    def __init__(self, width, height, clearance, side_of_hexagon):
        self.width = width
        self.height = height
        self.clearance = clearance
        self.side_of_hexagon = side_of_hexagon
        self.canvas = np.zeros((height, width, 3), dtype='uint8')
        self.horizontal_indices, self.vertical_indices = np.meshgrid(np.arange(self.height), np.arange(self.width), indexing='ij')
        self.clearance_color, self.obstacle_color = [255, 0, 0], [255, 255, 255]
        
    def define_hexagon(self):
        height_of_triangle = int((math.sqrt(3)/2) * self.side_of_hexagon)
        
        x1_c, y1_c = int(self.width/2 - height_of_triangle - self.clearance), int(self.height/2 - self.side_of_hexagon/2 - self.clearance/2)
        x2_c, y2_c = int(self.width/2), int(self.height/2 - self.side_of_hexagon - self.clearance)
        x3_c, y3_c = int(self.width/2 - height_of_triangle - self.clearance), int(self.height/2 + self.side_of_hexagon/2 + self.clearance/2)
        x4_c, y4_c = int(self.width/2), int(self.height/2 + self.side_of_hexagon + self.clearance)
        x5_c, y5_c = int(self.width/2 + height_of_triangle + self.clearance), int(self.height/2 + self.side_of_hexagon/2 + self.clearance/2)
        x6_c, y6_c = int(self.width/2 + height_of_triangle + self.clearance), int(self.height/2 - self.side_of_hexagon/2 - self.clearance/2)
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
    
    def define_triangle(self):
        x1_c, y1_c = 460 - self.clearance, 25 - self.clearance
        x2_c, y2_c = 460 - self.clearance, 225 + self.clearance
        x3_c, y3_c = 510 + 2 * self.clearance, 125 
        m1_c, m2_c = (y2_c - y3_c)/(x2_c - x3_c), (y1_c - y3_c)/(x1_c - x3_c)
        
        x1, y1 = 460, 35 
        x2, y2 = 460, 215
        x3, y3 = 510, 125 
        m1, m2 = (y2 - y3)/(x2 - x3), (y1 - y3)/(x1 - x3)
        for j in range(self.height):
            for i in range(self.width):
                if(i>=(460 - self.clearance) and ((j - m1_c*i - y3_c + m1_c*x3_c)<= 0 and (j - m2_c*i - y3_c + m2_c*x3_c)>= 0)):
                    self.canvas[j, i] = self.clearance_color
                if(i > (460) and ((j - m1*i - y3 + m1*x3)<= 0 and (j - m2*i - y3 + m2*x3)>= 0)):
                    self.canvas[j, i] = self.obstacle_color
        return
    
    def define_rectangle(self):
        x1_c, y1_c = 100 - self.clearance, 100 + self.clearance
        x2_c, y2_c = 150 + self.clearance, 100 + self.clearance
        x3_c, y3_c = 100 - self.clearance, 150 - self.clearance
        x4_c, y4_c = 150 + self.clearance, 150 - self.clearance
        
        x1, y1 = x1_c + self.clearance, y1_c - self.clearance
        x2, y2 = x2_c - self.clearance, y2_c - self.clearance
        x3, y3 = x3_c + self.clearance, y3_c + self.clearance
        x4, y4 = x4_c - self.clearance, y4_c + self.clearance
        
        for j in range(self.height):
            for i in range(self.width):
                if((i >= x1_c and i <= x2_c and j <= y1_c and j <= y2_c) or \
                    (i >= x3_c and i <= x4_c and j >= y3_c and j >= y4_c)):
                    self.canvas[j, i] = self.clearance_color
                if((i >= x1 and i <= x2 and j <= y1 and j <= y2) or \
                    (i >= x3 and i <= x4 and j >= y3 and j >= y4)):
                    self.canvas[j, i] = self.obstacle_color
        return
    
    def generate_map(self):
        self.define_hexagon()
        self.define_triangle()
        self.define_rectangle()
        return
    
    def display_map(self):
        map_to_display = self.canvas.copy()
        map_to_display_bgr = cv2.cvtColor(map_to_display, cv2.COLOR_RGB2BGR)
        cv2.imshow("Generated MAP", map_to_display_bgr)
        cv2.waitKey(5)
        return
    
    def get_map(self):
        return self.canvas
    
class Dijkstra:
    def __init__(self, initial_node, goal_node, obstacle_map):
        self.open_list = PriorityQueue()
        self.close_list = []
        self.cost_of_node = {}
        self.parent_node = {}
        self.found_path = []
        self.initial_node = initial_node
        self.goal_node = goal_node
        self.obstacle_map = obstacle_map
        
        self.open_list.put((0, self.initial_node))
        self.parent_node[self.initial_node] = None
        self.cost_of_node[self.initial_node] = 0  
        return
    
    def move_left(self, current_node):
        next_node = []
        next_node.append(current_node[0] - 1)
        next_node.append(current_node[1])
        return 1, tuple(next_node)
    
    def move_right(self, current_node):
        next_node = []
        next_node.append(current_node[0] + 1)
        next_node.append(current_node[1])
        return 1, tuple(next_node)
    
    def move_up(self, current_node):
        next_node = []
        next_node.append(current_node[0])
        next_node.append(current_node[1] - 1)
        return 1, tuple(next_node)
    
    def move_down(self, current_node):
        next_node = []
        next_node.append(current_node[0])
        next_node.append(current_node[1] + 1)
        return 1, tuple(next_node)
    
    def move_diag_left_bottom(self, current_node):
        next_node = []
        next_node.append(current_node[0] - 1)
        next_node.append(current_node[1] + 1)
        return 1.4, tuple(next_node)
    
    def move_diag_left_top(self, current_node):
        next_node = []
        next_node.append(current_node[0] - 1)
        next_node.append(current_node[1] - 1)
        return 1.4, tuple(next_node)
    
    def move_diag_right_bottom(self, current_node):
        next_node = []
        next_node.append(current_node[0] + 1)
        next_node.append(current_node[1] + 1)
        return 1.4, tuple(next_node)
    
    def move_diag_right_top(self, current_node):
        next_node = []
        next_node.append(current_node[0] + 1)
        next_node.append(current_node[1] - 1)
        return 1.4, tuple(next_node)
    
    def valid_next_move(self, current_node):
        valid_neighbors = []
        left = self.move_left(current_node)
        right = self.move_right(current_node)
        up = self.move_up(current_node)
        down = self.move_down(current_node)
        left_bottom = self.move_diag_left_bottom(current_node)
        left_top = self.move_diag_left_top(current_node)
        right_bottom = self.move_diag_right_bottom(current_node)
        right_top = self.move_diag_right_top(current_node)
        
        if(left[1][0] < 0 or left[1][0] > 599 or left[1][1] < 0 or left[1][1] > 249 or self.obstacle_map[left[1][1]][left[1][0]][0]==255):
            print("left neighbor invalid")
        else:
            valid_neighbors.append(left)
        
        if(right[1][0] < 0 or right[1][0] > 599 or right[1][1] < 0 or right[1][1] > 249 or self.obstacle_map[right[1][1]][right[1][0]][0]==255):
            print("right neighbor invalid")
        else:
            valid_neighbors.append(right)
            
        if(up[1][0] < 0 or up[1][0] > 599 or up[1][1] < 0 or up[1][1] > 249 or self.obstacle_map[up[1][1]][up[1][0]][0]==255):
            print("up neighbor invalid")
        else:
            valid_neighbors.append(up)
           
        if(down[1][0] < 0 or down[1][0] > 599 or down[1][1] < 0 or down[1][1] > 249 or self.obstacle_map[down[1][1]][down[1][0]][0]==255):
            print("down neighbor invalid")
        else:
            valid_neighbors.append(down)
           
        if(left_bottom[1][0] < 0 or left_bottom[1][0] > 599 or left_bottom[1][1] < 0 or left_bottom[1][1] > 249 or self.obstacle_map[left_bottom[1][1]][left_bottom[1][0]][0]==255):
            print("left_bottom neighbor invalid")
        else:
            valid_neighbors.append(left_bottom)
        
        if(left_top[1][0] < 0 or left_top[1][0] > 599 or left_top[1][1] < 0 or left_top[1][1] > 249 or self.obstacle_map[left_top[1][1]][left_top[1][0]][0]==255):
            print("left_top neighbor invalid")
        else:
            valid_neighbors.append(left_top)
            
        if(right_bottom[1][0] < 0 or right_bottom[1][0] > 599 or right_bottom[1][1] < 0 or right_bottom[1][1] > 249 or self.obstacle_map[right_bottom[1][1]][right_bottom[1][0]][0]==255):
            print("right_bottom neighbor invalid")
        else:
            valid_neighbors.append(right_bottom)
            
        if(right_top[1][0] < 0 or right_top[1][0] > 599 or right_top[1][1] < 0 or right_top[1][1] > 249 or self.obstacle_map[right_top[1][1]][right_top[1][0]][0]==255):
            print("right_top neighbor invalid")
        else:
            valid_neighbors.append(right_top)
        return valid_neighbors