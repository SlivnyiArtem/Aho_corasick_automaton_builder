import networkx as nwx
import matplotlib.pyplot as plt


def visualize_graph(edge_dictionary):
    graph = nwx.DiGraph()
    graph.add_edges_from(edge_dictionary.keys())
    graph_pos = nwx.planar_layout(graph)
    nwx.draw_planar(graph, with_labels=True)
    nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=edge_dictionary)
    plt.show()
