from garbage_code.service_funcs import check_all_postfix


class AhoKorasicNode(object):
    def __init__(self, current_string, input_abc, input_prefixes):
        self.value = current_string
        self.abc = input_abc
        self.suffix_link = self.get_suffix_link(input_prefixes)
        self.prefix_links = {}
        for command_symb in input_abc:
            new_word = current_string + command_symb
            best_postfix = check_all_postfix(new_word, input_prefixes)
            self.prefix_links[command_symb] = "\u03bb" if best_postfix is None else best_postfix

    def get_suffix_link(self, input_prefixes):
        for i in range(1, len(self.value)):
            if self.value[i:] in input_prefixes:
                return self.value[i:]
