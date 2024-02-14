import cv2

class RecordVideo:
    def __init__(self, path, map, file_path):
        self.path = path
        self.map = map
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(file_path, self.fourcc, 60, (map.shape[1], map.shape[0]))
        
    def run(self):
        for x, y in self.path:
            self.map[y, x, 1] = 255
            self.video.write(self.map)
        return