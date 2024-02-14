from queue import PriorityQueue

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
    
    def run(self):
        while self.open_list:
            current_node = self.open_list.get()[1]
            self.close_list.append(current_node)
            if current_node == self.goal_node:
                print("\n.. Goal Reached .. \n")
                break
            else:
                valid_neighbors = self.valid_next_move(current_node)
                for next_node in valid_neighbors:
                    if(next_node[1] in self.close_list):
                        continue
                    else:
                        cost_to_next_node = next_node[0]
                        total_cost_to_node = self.cost_of_node[current_node] + cost_to_next_node
                        if (next_node[1] not in self.cost_of_node or total_cost_to_node < self.cost_of_node[next_node[1]]):
                            self.cost_of_node[next_node[1]] = total_cost_to_node
                            self.open_list.put((total_cost_to_node, next_node[1]))
                            self.parent_node[next_node[1]] = current_node
        return
    
    def get_generated_path(self):
        end_node = self.goal_node
        while end_node != None:
            self.found_path.append(end_node)
            end_node = self.parent_node[end_node]
        self.found_path.reverse()
        return self.found_path