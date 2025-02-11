class TreeNode:
    def __init__(self, parent_nodes,tour, tour_distance):
        self.parent_nodes = parent_nodes
        self.child_nodes = None

        self.tour = tour
        self.tour_distance = tour_distance
