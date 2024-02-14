class UserInput:
    def __init__(self, obstacle_map):
        self.goal_node = None
        self.initial_node = None
        self.obstacle_map  = obstacle_map
        
    def enter_coordinates(self):
        x_initial = int(input("Enter initial x-coordinate"))
        y_initial = int(input("Enter initial y-coordinate"))
        x_goal = int(input("Enter goal x-coordinate"))
        y_goal = int(input("Enter goal y-coordinate"))
        initial_node = (x_initial, self.obstacle_map.shape[0] - y_initial - 1)
        goal_node = (x_goal, self.obstacle_map.shape[0] - y_goal - 1)
        return initial_node, goal_node
    
    def check_valid_entry(self):
        if(
        self.obstacle_map[self.initial_node[1]][self.initial_node[0]][0]==255 or \
        self.obstacle_map[self.goal_node[1]][self.goal_node[0]][0]==255 or \
        self.initial_node[0] < 0 or \
        self.initial_node[0] > 599 or \
        self.initial_node[1] < 0 or \
        self.initial_node[1] > 249 or \
        self.goal_node[0] < 0 or \
        self.goal_node[0] > 599 or \
        self.goal_node[1] < 0 or \
        self.goal_node[1] > 249 or \
        sum(self.obstacle_map[self.initial_node[1]][self.initial_node[0]])==765 or \
        sum(self.obstacle_map[self.goal_node[1]][self.goal_node[0]])==765
        ):
            print("The start point or end point is invalid. Either it is out of bounds or within obstacle space. Try Again!\n")
            return False
        else:
            print("Great! The start and goal points are valid")
            return True
        
    def take_input(self):
        self.initial_node, self.goal_node = self.enter_coordinates()
        while(not self.check_valid_entry()):
            self.initial_node, self.goal_node = self.enter_coordinates()
        return self.initial_node, self.goal_node