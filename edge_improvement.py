class EdgeImprovement:
    def __init__(self, node_id, improvement):
        self.node_id = node_id
        self.improvement = improvement

    def __lt__(self, other):
        return self.improvement < other.improvement