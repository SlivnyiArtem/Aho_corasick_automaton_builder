import random
import re

import pandas as pd
from dash_bootstrap_components import Table
from dash import dash_table


def generate_lambda_table(nodes: dict):
    data = list(map(lambda node:
                    (node.value, node.suffix_link if node.suffix_link is not None else "None"), nodes.values()))
    df = pd.DataFrame(data, columns=["prefix", "suffix_link"])
    table = Table.from_dataframe(df, index=True, striped=True, bordered=True, hover=True)
    table = dash_table.DataTable(data=df.to_dict('records'), style_cell={'textAlign': 'left'},)
    return table


def generate_table(table_dict):
    cur_df = pd.DataFrame()
    for item in table_dict.keys():
        prefix, value = item
        cur_df.loc[prefix, table_dict[item]] = value

    table = Table.from_dataframe(cur_df, index=True, striped=True, bordered=True, hover=True)
    #
    # table = dash_table.DataTable(data = cur_df.to_dict('index'), style_cell={'textAlign': 'left'},)
    #?????
    return table


def generate_random_words(lexem_length: int, random_list_len: int):
    common_lexem = generate_random_lexem(lexem_length)
    miss_cnt = 0
    result_set = set()
    with open('../singular.txt', 'r', encoding="utf-8") as f:
        words = f.readlines()
    words = [s.strip("\n") for s in words]
    while True:
        if len(result_set) == random_list_len:
            break
        random_word: str = random.choice(words)
        if re.search(common_lexem, random_word) is not None:
            result_set.add(random_word)
        else:
            miss_cnt += 1
            if miss_cnt == 1000:
                common_lexem = generate_random_lexem(lexem_length)
                miss_cnt = 0
    return result_set


def generate_random_lexem(lexem_length):
    vowels = 'уеыаоэяию'
    consonants = 'йцкнгшщзхфвпрлджчсмтб'
    res = []
    for i in range(lexem_length):
        res.append(random.choice(consonants) if i % 2 == 0 else random.choice(vowels))
    return "".join(res)
