import networkx as nwx
import matplotlib.pyplot as plt


def visualize_graph(edge_dictionary):
    graph = nwx.DiGraph()
    graph.add_edges_from(edge_dictionary.keys())
    graph_pos = nwx.spring_layout(graph, k=500, iterations=100)
    nwx.draw(graph, graph_pos, with_labels=True)
    nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=edge_dictionary)
    plt.show()
