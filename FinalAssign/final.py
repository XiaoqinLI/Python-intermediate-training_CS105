import random
from optparse import *
import enum
import re
import urllib
import pickle
import logging
import graph
import collections
import types
import urllib.request
import sys
import string
from pprint import pprint


line_re = re.compile(r"(?P<node_id>\d+):\s*(?P<edges>.*)$")
edge_re = re.compile(r"\((?P<token>\"[^\"]*\"|[\d.]+),\s*(?P<probability>[\d.]+),\s*(?P<target>[\d]+)\)")

def parse_line1(line, cache_dict):
    line_match = line_re.match(line)
    node_id, edge_str = line_match.group("node_id", "edges")
    node_id = int(node_id)
    edges = edge_re.finditer(edge_str)
    node = graph.MarkovChainNode(node_id)  # now state is None obj
    if not node_id in cache_dict:
        cache_dict[node_id] = None
    for edge_match in edges:
        token_str, prob_str, target_str = edge_match.group("token", "probability", "target")
        target_str =  int(target_str)
        if token_str[0] == '"':
            token = token_str[1:-1]
        else:
            token = float(token_str) if "." in token_str else int(token_str)
        if type(token) ==  str and token.isdigit():
             token = float(token) if "." in token_str else int(token)
        cache_dict[target_str] = token
    return int(node_id), node


def parse_line2(line, nodes):
    line_match = line_re.match(line)
    node_id, edge_str = line_match.group("node_id", "edges")
    node_id = int(node_id)
    edges = edge_re.finditer(edge_str)
    for edge_match in edges:
        token_str, prob_str, target_str = edge_match.group("token", "probability", "target")
        target_str =  int(target_str)
        if token_str[0] == '"':
            token = token_str[1:-1]
        else:
            token = float(token_str) if "." in token_str else int(token_str)
        if type(token) ==  str and token.isdigit():
            token = float(token) if "." in token_str else int(token)

        prob = float(prob_str)
        followerNode = nodes[target_str]
        nodes[node_id].add_next_state(followerNode,prob)


def parse_lines(lines):
    cache_dict = dict()
    nodes = dict(parse_line1(line, cache_dict) for line in lines)
    for key in cache_dict:
        nodes[key].state = (cache_dict[key],)
    for line in lines:
        parse_line2(line, nodes)
    return nodes


class TrainingErrorException(Exception):
    """Create an exception TrainingError that has an attribute tokens_loaded."""
    def __init__(self, err, tokens_loaded=0):
        self.err = err
        self.tokenLoaded = tokens_loaded
    def __str__(self):
        return self.err + ". {} tokens were loaded".format(self.tokenLoaded)


class Tokenization(enum.Enum):
    """ tokenization modes
    word: Interpret the input as UTF-8 and split the input at any Unicode
    white-space characters and use the strings between the white-space
    as tokens. So "a b" would be [a, b] as would "a\nb" and "a \u00A0\nb"
    (\u00A0 is non-breaking space).

    character: Interpret the input as UTF-8 and use the characters as tokens.

    byte: Read the input as raw bytes and use individual bytes as the tokens.

    none: Do not tokenize. The input must be an iterable.
    """
    word = 1
    character = 2
    byte = 3
    none = 4


class RandomWriter(object):
    """A Markov chain based random data generator."""

    def __init__(self, level=1, tokenization=Tokenization.none):
        """Initialize a random writer.
        Args:
          level: The context length or "level" of model to build.
          tokenization: A value from Tokenization. This specifies how
            the data should be tokenized.
        The value given for tokenization will affect what types of
        data are supported.
        """
        self.level = level
        self.tokenization = tokenization
        self.model = graph.MarkovChainGraph()

    def generate(self):
        """Generate tokens using the model."""
        node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]
        while len(node.next_states) == 0:
            node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]

        while True:
            yield node.state[-1]
            if len(node.next_states) != 0:
                node = node.get_next_state()
                if node == None:
                    node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]
                    while len(node.next_states) == 0:
                        node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]
            else:
                node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]
                while len(node.next_states) == 0:
                    node = self.model.chain[random.choice([key for key in self.model.chain.keys()])]


    def generate_file(self, filename, amount):
        """Write a file using the model.
        Args:
          filename: The name of the file to write output to.
          amount: The number of tokens to write.
        Make sure to open the file in the appropriate mode.
        """
        if type(amount == str):
            amount = int(amount)
        ####----------------------------------##############
        #######this is for sys.stdout file object
        if hasattr(filename, 'read'):
            fi = filename
            for ele in self.generate():
                if self.tokenization == Tokenization.byte:
                    fi.write(bytes(chr(ele),'utf-8'))
                if self.tokenization == Tokenization.character:
                    fi.write(ele)
                elif self.tokenization == Tokenization.word:
                    fi.write(ele+" ")
                elif self.tokenization == Tokenization.none:
                    ele = str(ele)
                    fi.write(ele+" ")
                amount -= 1
                if amount <= 0:
                    break
        ####################################################
        if self.tokenization == Tokenization.byte:
            with open(filename, mode="wb") as fi:
                for ele in self.generate():
                    fi.write(bytes(chr(ele),'utf-8'))
                    amount -= 1
                    if amount <= 0:
                        break
        else:
            with open(filename, encoding = 'utf-8', mode="w") as fi:
                for ele in self.generate():
                    if self.tokenization == Tokenization.character:
                        fi.write(ele)
                    elif self.tokenization == Tokenization.word:
                        fi.write(ele+" ")
                    elif self.tokenization == Tokenization.none:
                        ele = str(ele)
                        fi.write(ele+" ")
                    amount -= 1
                    if amount <= 0:
                        break

    def save_text(self, filename_or_file_object):
        """Write the model to a text file.
        If the model is not a word, character, or byte model then this
        data file will not allow this model to be rebuild
        exactly. Instead the new model will have string
        representations instead of the original tokens. This is
        expected.
        Training is not supported on models loaded form text files
        """

        if hasattr(filename_or_file_object, 'read'):
            fi = filename_or_file_object
        else:
            fi = open(filename_or_file_object, encoding = 'utf-8', mode="w")
        for key in self.model.chain:
            outputStr = str(key) + ":"
            targetStr = ""
            if len(self.model.chain[key].next_states) == 0:
                fi.write(outputStr)
                fi.write("\n")
                continue     # skipped the ones without followers
            for ele in self.model.chain[key].next_states:
                if self.tokenization == Tokenization.none:
                    state = "\""+repr(ele[0].state[-1]) + "\"" # none mode
                elif self.tokenization == Tokenization.byte:
                    state = "\""+repr(ele[0].state[-1]) + "\"" # none mode
                else:
                    state = "\""+ele[0].state[-1] + "\""    # word or charracter

                prob = str(ele[1])
                value = str(ele[0].value)
                eleStr = "(" + ", ".join((state, prob, value)) + ")"
                targetStr = " ".join((targetStr,eleStr))
            outputStr += targetStr
            fi.write(outputStr)
            fi.write("\n")
        fi.close()

    @classmethod
    def load_text(cls, filename_or_file_object):
        """Load a model from a text file in the same format as used for
        save_text.
        Args:
          filename_or_file_object: A filename or file object to load
            from. You need to support both.
        If the argument is a file object you can assume it is opened
        in text mode.
        This should construct a new RandomWriter instance.
        """

        if hasattr(filename_or_file_object, 'read'):
            fi = filename_or_file_object
        else:
            fi = open(filename_or_file_object, encoding = 'utf-8', mode="rt")
        lines = fi.readlines()
        fi.close()
        for i in range(len(lines)):
            lines[i] = lines[i][:-1]
        model = parse_lines(lines)
        rw = RandomWriter()
        rw.model.chain = model
        return rw

    def save_pickle(self, filename_or_file_object):
        """Write this model out as a Python pickle."""

        if hasattr(filename_or_file_object, 'read'):
            fi = filename_or_file_object
        else:
            fi = open(filename_or_file_object, 'wb')
        pickle.dump(self.model.chain, fi)
        fi.close()

    @classmethod
    def load_pickle(cls, filename_or_file_object):
        """Load a Python pickle and make sure it is in fact a model."""

        if hasattr(filename_or_file_object, 'read'):
            fi = filename_or_file_object
        else:
            fi = open(filename_or_file_object, 'rb')
        rw = RandomWriter()
        rw.model.chain = pickle.load(fi)
        fi.close()
        return rw

    @classmethod
    def load(cls, filename):
        """Load a model from a file that may be a pickle or a text file.
        This should not duplicate any code in the other load methods.
        """

        try:
            return RandomWriter.load_pickle(filename)
        except pickle.UnpicklingError:
            logging.warning("It is not a pickle object, will load it as a normal file")
            return RandomWriter.load_text(filename)

    def train_url(self, url):
        """Compute the probabilities based on the data downloaded from url.
        This method is only supported if the tokenization mode is not
        none.
        Training is not supported on models loaded form text files.
        """

        if self.tokenization == Tokenization.none:
            raise TrainingErrorException("train_url only supported if the tokenization mode is not none.")
        try:
            infile = urllib.request.urlopen(url)

            # data = (str(line, encoding= 'utf8') for line in infile.readlines())
            data = str(infile.read(),encoding= 'utf8')
            self.train_iterable(data)
        except urllib.error.HTTPError:
            logging.error("The web link is not correct")
        except urllib.error.URLError:
            logging.error("The internet may not be connected yet")

    def train_iterable(self, data):
        """Compute the probabilities based on the data given.
        Training is not supported on models loaded form text files.
        """

        if not isinstance(data, types.GeneratorType):
            if self.tokenization == Tokenization.character:
                if type(data) != str:
                    raise TypeError
            elif self.tokenization == Tokenization.word:
                if type(data) != str:
                    raise TypeError
                else:
                    data = tuple(data.split())
            elif self.tokenization == Tokenization.byte:
                if type(data) != bytes:
                    raise TypeError
            else:
                if not isinstance(data, collections.Iterable):
                    raise TypeError
        try:
            tokens = {}
            for i,j in self.windowed(data, self.level):
                token = tuple(i)
                if not token in tokens:
                    tokens[token] = {}
                follower = (j,)
                if follower[0] != None:
                    tokens[token][follower] = tokens[token][follower] + 1 if follower in tokens[token] else 1
            if len(tokens) == 1:
                raise Exception("The data is too short, should have provided more than {} elements".format(self.level))
        except Exception:
            raise TrainingErrorException("There is an error occurs while loading trainingdata", len(tokens))

        self.build_markov_chain(tokens)

    def windowed(self, iterable, size):
        window = list()
        for v in iterable:
            if len(window) < size+1:
                window.append(v)
            else:
                window.pop(0)
                window.append(v)
            if len(window) == size+1:
                yield window[:-1], window[-1]
        yield (window[1:], None)

    def build_markov_chain(self, tokens):
        autoCounter = 1
        for token in tokens:
            self.model.add_node(autoCounter, token)
            autoCounter += 1
        for token, followers in tokens.items():
            if len(followers)>0:
                weight = float(sum((count for follower, count in followers.items())))
                for follower, count in followers.items():
                    next_state_token = token[1:] + follower

                    for item in self.model.chain.values():
                        if item.state == next_state_token:
                            next_state_token_ID = item.value
                            break
                    for item in self.model.chain.values():
                        if item.state == token:
                            current_token_ID = item.value
                            break

                    if next_state_token_ID in self.model.chain:
                        next_state_node = self.model[next_state_token_ID]
                        self.model[current_token_ID].add_next_state(next_state_node, count/weight)

if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option("-t", "--train", action="store_true", dest="train",
                      help = "Train a model using the given input and save it to a text format output file.")
    parser.add_option("-g", "--generate", action="store_true", dest="generate",
                      help = "Train a model using the given input and save it to a text format output file.")

    parser.add_option("-i", "--input", dest = "input",
                      help = "The input file to train on (Default standard input).")
    parser.add_option("-o", "--output", dest = "output",
                      help = "The output file to save the model to (Default standard output).")
    # parser.add_option("-s", "--console", dest = "console", default=True,
    #                   help = "print the output to console.")
    parser.add_option("-l", "--level", dest = "level",
                      help = "Train for level n (Default 1).")
    parser.add_option("-a", "--amount", dest = "amount",
                      help = "Generate n tokens of output (Required).")

    parser.add_option("-w", "--word", action="store_true", dest="word",
                      help = "Use word tokenization (Default)")
    parser.add_option("-c", "--character", action="store_true", dest = "character",
                      help = "Use character tokenization")
    parser.add_option("-b", "--byte", action="store_true", dest = "byte",
                      help = "Use byte tokenization")

    options, args = parser.parse_args()

    rw = RandomWriter(1, Tokenization.word)

    if options.train is None and options.generate is None:
        logging.error("Either source file or MarkovChain model file should be specified!")

    elif options.train is not None and options.generate is not None:
        logging.error("Source file and MarkovChain model file cannot be used at the same time!")

    elif options.train is not None:  # dealing with train.

        if options.input is None:
            logging.error("No input source data specified")


        else:
            if options.level is not None:
                rw.level = int(options.level)

            if all((options.character is None, options.word is None, options.byte is None)) or (options.word is not None and all([ options.character is None, options.byte is None])):
                rw.train_url(options.input)
            elif(options.character is not None and all([ options.word is None, options.byte is None])):
                rw.tokenization = Tokenization.character
                rw.train_url(options.input)
            elif(options.byte is not None and all([ options.word is None, options.character is None])):
                rw.tokenization = Tokenization.byte
                rw.train_url(options.input)
            else:
                logging.error("wrong tokenization specification")

            if options.output is not None:
                rw.save_text(options.output)
            else:
                rw.save_text(sys.stdout)

    else:
        if options.input is None:
            logging.error("No input model specified")
        elif options.amount is None:
            logging.error("No number of tokens of output specified")

        elif options.output is None:
            rw = RandomWriter.load(options.input)
            rw.generate_file(sys.stdout, options.amount)

        else:
            rw = RandomWriter.load(options.input)
            rw.generate_file(options.output, options.amount)

#################################################################################################################################
#######Do not have time to figure this out since I have other projects due and need to work more than 30 hours a week ###########
#python3 final.py --train --character --input file://input.file | python3 final.py --generate --amount 1024 --output output.file
##################################Hope this won't take too much points off#######################################################
######################This project is very educational but also a bit advanced to me to finish it in 4 days#####################


