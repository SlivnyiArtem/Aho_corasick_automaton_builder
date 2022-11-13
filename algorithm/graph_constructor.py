import networkx as nwx
import matplotlib.pyplot as plt


def form_graph(edge_dictionary):
    graph = nwx.DiGraph()
    graph.add_edges_from(edge_dictionary.keys())
    # draw_gr(graph, edge_dictionary)
    return graph


def draw_gr(graph, edge_dictionary):
    graph_pos = nwx.planar_layout(graph)
    nwx.draw_planar(graph, with_labels=True)
    nwx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=edge_dictionary)
    fig, ax = plt.subplots()
    ax = fig.add_axes([0.81, 0.05, 0.1, 0.075])
    # button
    plt.show()
