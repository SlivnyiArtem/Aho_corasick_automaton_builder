import Aho_Korasic_Node
import service_funcs


def main():
    input_data = str(input())
    prefixes = service_funcs.get_prefixes(service_funcs.get_words_from_str(input_data))
    abc = service_funcs.get_abc_from_str(input_data)
    node_dict = {}
    for prefix in prefixes:
        node = Aho_Korasic_Node.AhoKorasicNode(prefix, abc, prefixes)
        node_dict[node.value] = node
    '''
    Aho_Korasic_Node.AhoKorasicNode("кас", service_funcs.get_abc_from_str(input_data),
                                    service_funcs.get_prefixes
                                    (service_funcs.get_words_from_str(input_data)))
    '''


if __name__ == '__main__':
    main()
#if __name__ == "__main__":
#    calculate(str(input()))
