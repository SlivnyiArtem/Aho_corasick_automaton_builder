import networkx as nwx
import matplotlib.pyplot as plt


def form_graph(edge_dictionary):
    graph = nwx.DiGraph()
    graph.add_edges_from(edge_dictionary.keys())
    return graph
