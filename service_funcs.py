from collections import defaultdict


def get_abc_from_str(input_str):
    abc = set(input_str)
    if " " in abc:
        abc.remove(" ")
    return sorted(abc)


def get_words_from_str(input_str):
    return input_str.split()


def get_prefixes(words):
    prefixes_list = []
    for word in words:
        for i in range(1, len(word) + 1):
            prefixes_list.append(word[:i])
    return prefixes_list


def create_node_dict(labels):
    node_dict = defaultdict(list)
    for start, end in labels.keys():
        node_dict[start].append(end)
    return node_dict
