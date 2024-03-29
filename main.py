from helper.map import Map
from helper.dijkstra import Dijkstra
from helper.user_input import UserInput
from utils.plot import RecordVideo

if __name__ == "__main__":
    map = Map(600, 300, 5, 75)
    map.generate_map()
    map.display_map()
    obstacle_map = map.get_map()
    
    input = UserInput(obstacle_map)
    initial_node, goal_node = input.take_input()
    
    dijkstra = Dijkstra(initial_node, goal_node, obstacle_map)
    dijkstra.run()
    found_path = dijkstra.get_generated_path()
    
    record = RecordVideo(found_path, obstacle_map, "./test_case/test_case.avi")
    record.run()