import random
import re
import dash_bootstrap_components as dbc

import pandas as pd

from garbage_code.cyto_data import Singletone
from process import AhoKorasicProcessWindow


def get_random_lexem(lexem_length):
    vowels = 'уеыаоэяию'
    consonants = 'йцкнгшщзхфвпрлджчсмтб'
    res = []
    for i in range(lexem_length):
        res.append(random.choice(consonants) if i % 2 == 0 else random.choice(vowels))
    return "".join(res)


def get_random_words(lexem_length: int, random_list_len: int):
    common_lexem = get_random_lexem(lexem_length)
    miss_cnt = 0
    result = set()
    with open('../singular.txt', 'r', encoding="utf-8") as f:
        words = f.readlines()
    words = [s.strip("\n") for s in words]
    while True:
        if len(result) == random_list_len:
            break
        random_word: str = random.choice(words)
        if re.search(common_lexem, random_word) is not None:
            result.add(random_word)
        else:
            miss_cnt += 1
            if miss_cnt == 1000:
                common_lexem = get_random_lexem(lexem_length)
                miss_cnt = 0
    return result


# def copy_to_excel(path_to_excel: str):
#     global cur_df
#     cur_df.to_excel(path_to_excel)


def generate_table(table_dict):
    cur_df = pd.DataFrame()
    for item in table_dict.keys():
        prefix, value = item
        cur_df.loc[prefix, table_dict[item]] = value
    table = dbc.Table.from_dataframe(cur_df, index=True)
    return table, cur_df


def generate_graph(S: Singletone):
    _, visualize_dict, _, _, _, node_dict = AhoKorasicProcessWindow.calculate("рама мара")

    visited_nodes = set()

    cy_edges = []
    cy_nodes = []

    for source in node_dict.keys():
        node_targets = node_dict[source]
        for target in node_targets:
            if source not in visited_nodes:
                visited_nodes.add(source)
                cy_nodes.append({"data": {"id": source, "label": source}})
            if target not in visited_nodes:
                visited_nodes.add(target)
                cy_nodes.append({"data": {"id": target, "label": target}})

            cy_edges.append({"data": {"source": source, "target": target, "label": visualize_dict[(source, target)]}})

    # return DataStage(visualize_dict, node_dict, cy_nodes, cy_edges)
    S.update_singleton(visualize_dict, node_dict, cy_edges, cy_nodes)
    # i()
