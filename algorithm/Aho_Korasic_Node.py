class AhoKorasicNode(object):

    def __init__(self, current_string, input_abc, input_prefixes):
        self.value = current_string
        self.abc = input_abc
        self.suffix_link = self.get_suffix_link(input_prefixes)
        self.prefix_links = {}
        for command_word in input_abc:
            new_word = current_string + command_word
            if new_word in input_prefixes:
                self.prefix_links[command_word] = new_word
            elif command_word in input_prefixes:
                self.prefix_links[command_word] = command_word
            else:
                self.prefix_links[command_word] = "lambda"

        print(self.value)
        print(self.abc)
        print(self.suffix_link)
        print(self.prefix_links)

    def get_suffix_link(self, input_prefixes):
        for i in range(1, len(self.value)):
            if self.value[i:] in input_prefixes:
                return sorted(self.value[i:])
