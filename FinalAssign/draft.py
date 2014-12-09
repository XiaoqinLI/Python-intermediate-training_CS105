# import enum
# class Tokenization(enum.Enum):
#     """ tokenization modes
#     word: Interpret the input as UTF-8 and split the input at any Unicode
#     white-space characters and use the strings between the white-space
#     as tokens. So "a b" would be [a, b] as would "a\nb" and "a \u00A0\nb"
#     (\u00A0 is non-breaking space).
#
#     character: Interpret the input as UTF-8 and use the characters as tokens.
#
#     byte: Read the input as raw bytes and use individual bytes as the tokens.
#
#     none: Do not tokenize. The input must be an iterable.
#     """
#     word = 1
#     character = 2
#     byte = 3
#     none = 4
#
# a = Tokenization(4)
# print(a == Tokenization.none)
# b = "asdaf"
# print (type(b))
# print (type(b) == str)
#
# c = bytes(b)
#
# print (c)
# print(type(c))
#
# import re
# pattern = r'\s+'
# a ="a b".split()
# b = "a\nb".split()
# c = "a \u00A0\nb".split()
# # "a b" would be [a, b] as would "a\nb" and "a \u00A0\nb"
# print (a)
# print (b)
# print (c)

# my_str = "hello world"
# bytes = str.encode(my_str)
# print(bytes)
# print(type(bytes)) # insures its bytes
# # my_decoded_str = str.decode(bytes)
# # print(type(my_decoded_str))# insures its string

# import binascii
# binary = '\x5A\x05\x70\x5D\xC2\x5C\xA1\x51\x23\xC8\xE4\x75\x0B\x80\xD0\xA9'
# print(type(binary))

# binary = binascii.unhexlify("helloworld")
# print(type(binary))

# mm = b'abcdefghiab'
# print(type(mm))
#
# a = mm[3:4]
# print (a)

# import collections
# aaa = (i for i in range(10))
# print (aaa)
# print(type(aaa))
# print(isinstance(aaa, collections.Iterable))

# import re
# line_re = re.compile(r"(?P<node_id>\d+):\s*(?P<edges>.*)$")
# edge_re = re.compile(r"\((?P<token>\"[^\"]*\"|[\d.]+),\s*(?P<probability>[\d.]+),\s*(?P<target>[\d]+)\)")
# print("")
# def parse_line(line):
#     line_match = line_re.match(line)
#     node_id, edge_str = line_match.group("node_id", "edges")
#     edges = edge_re.finditer(edge_str)
#     node = final.graph.Node()
#     for edge_match in edges:
#         token_str, prob_str, target_str = edge_match.group("token", "probability", "target")
#         if token_str[0] == '"':
#             token = token_str[1:-1]
#         else:
#             token = float(token_str) if "." in token_str else int(token_str)
#         edge = node.get_edge(token, int(target_str))
#         edge.probability = float(prob_str)
#     return int(node_id), node
#
# def parse_lines(lines):
#     nodes = dict(parse_line(line) for line in lines)
#     for node in nodes.values():
#         for edge in node.out_edges:
#             edge.target = nodes[edge.target]
#     return set(nodes.values())

 # if isinstance(data, types.GeneratorType):
        #     for i,j in self.windowed(data, self.level):
        #         token = tuple(i)
        #         if not token in tokens:
        #             tokens[token] = {}
        #         follower = (j,)
        #         if follower[0] != None:
        #             tokens[token][follower] = tokens[token][follower] + 1 if follower in tokens[token] else 1
        # else:
        #     dataLength = len(data)
        #     if dataLength < self.level:
        #         raise Exception("The data is too short, should have provided more than {} elements".format(self.level))
        #     for i in range(dataLength - self.level + 1):
        #         token = tuple(data[i: i + self.level]) #if i + self.level < dataLength else data[i: dataLength] + data[0: (self.level - (dataLength - i))]
        #         if not token in tokens:
        #             tokens[token] = {}
        #         if i < dataLength - self.level:
        #             follower = tuple(data[i + self.level:i + self.level+1])
        #             ############### watch out unhashable key######################
        #             tokens[token][follower] = tokens[token][follower] + 1 if follower in tokens[token] else 1
#
# def bb(x,c):
#     c[x] = x
#
# def aa():
#     a = {}
#     bb(2,a)
#     print (a)
#
# aa()

print( """\
1: ("a", 0.5, 2) ("b", 0.5, 3)
2: ("c", 1, 1)
3: ("c", 1, 1)
""")