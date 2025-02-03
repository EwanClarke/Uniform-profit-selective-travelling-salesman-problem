from math import sqrt


class Node:
    def __init__(self, nodeId, random_x, random_y):
        self.id = nodeId
        self.x = random_x
        self.y = random_y

    def calculate_distance(self, other_path):
        x_difference = self.x - other_path.x
        y_difference = self.y - other_path.y
        return sqrt(x_difference**2 + y_difference**2)

    def get_node_id(self):
        return self.id
