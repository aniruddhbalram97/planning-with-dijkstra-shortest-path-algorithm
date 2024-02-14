from helper.helper import Map
from helper.helper import Dijkstra
from helper.helper import Input

if __name__ == "__main__":
    map = Map(600, 300, 5, 75)
    map.generate_map()
    map.display_map()
    obstacle_map = map.get_map()
    
    input = Input(obstacle_map)
    initial_node, goal_node = input.take_input()
    
    dijkstra = Dijkstra(initial_node, goal_node, obstacle_map)
    dijkstra.run()
    found_path = dijkstra.get_generated_path()
    print(found_path)
    