from typing import List
from algorithm import Aho_Korasic_Node

from prettytable import PrettyTable


def visualize_table(columns_list, nodes_list: List[Aho_Korasic_Node.AhoKorasicNode]):
    table = PrettyTable()
    fin_columns_list = ['NodeValue']
    fin_columns_list += columns_list
    fin_columns_list.append('suffix_link')
    table.field_names = fin_columns_list
    for node in nodes_list:
        res_list = [node.value]
        res_list += list(node.prefix_links.values())
        res_list.append(node.suffix_link)
        table.add_row(res_list)
    print(table)
