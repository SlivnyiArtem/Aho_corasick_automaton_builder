class Singletone:
    def __init__(self):
        self.V = None
        self.node_dict = None
        self.cy_edges = []
        self.cy_nodes = []

    def update_singleton(self, v_dict, n_dict, cur_edges, cur_nodes):
        self.V = v_dict
        self.node_dict = n_dict
        self.cy_nodes = cur_nodes
        self.cy_edges = cur_edges
