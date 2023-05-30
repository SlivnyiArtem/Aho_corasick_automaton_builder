from algorithm import Aho_Korasic_Node, graph_constructor, service_funcs


def calculate(input_data: str):
    # input_data = text
    prefixes = service_funcs.get_prefixes(service_funcs.get_words_from_str(input_data))
    abc = service_funcs.get_abc_from_str(input_data)
    node_dict = {}
    visualize_dict = {}
    for prefix in prefixes:
        node = Aho_Korasic_Node.AhoKorasicNode(prefix, abc, prefixes)
        start_node = node.value[:-1]
        if start_node == "":
            start_node = "NullNode"
        visualize_dict[(start_node, node.value)] = node.value[-1]
        node_dict[node.value] = node

    for node in node_dict.values():
        if node.suffix_link is not None:
            visualize_dict[(node.value, node.suffix_link)] = "\u03bb"
        else:
            visualize_dict[(node.value, "NullNode")] = "\u03bb"
    graph = graph_constructor.form_graph(visualize_dict)
    return graph, visualize_dict, prefixes, node_dict, abc, service_funcs.create_node_dict(visualize_dict)
