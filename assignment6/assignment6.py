"""Implement a class called TreeDict that supports operators the same
way as a dict. 

TreeDict should be implemented using the binarysearchtree module I
have provided (you can download it from canvas in the same folder as
this file).

You need to make sure you support the following operations with the
same semantics as a normal Python dict:
* td[key]
* td[key] = value
* key in td
* td.get(key)
* td.get(key, default)
* del td[key]
* td.update(iterable_of_pairs_or_dict_or_td)
* td.update(key1=value1, key2=value2, ...)
* len(td)
* for key in td: pass
* for key, value in td.items(): pass
* for value in td.values(): pass

Iteration should be in key order, this should be pretty easy to do
just by traversing the tree using an in-order traversal. None of the
iterator methods should make a copy of any of the data in the
TreeDict.

You should support a constructor which takes the same arguments as
update and creates a TreeDict with just those values. There is an easy
way to do this in just a couple of lines using your existing update
method.

For each operation, make sure it does the same thing as a dict and you
handle errors by throwing the same type of exception as would be throw
by a dict. However unlike dict your implementation will not support
None as a key and you should throw an appropriate exception if None is
used as a key. Look at the available built in exceptions and pick the
most appropriate one you find.

Most of these methods will be very short (just a couple of lines of
code), a couple will be a bit more complicated. However all the hard
work should already be handled by the binarysearchtree module. It
looks like a lot of operations, but it shouldn't actually take that
long. Many of the operations are quite similar as well.

Do not reimplement anything in the binarysearchtree module or copy
code from it. You should not need to.

For this assignment I expect you will have to use at least the
following things you have learned:
* Raising exceptions
* Catching exceptions
* Implementing magic methods
* Generators using yield (and you may want to look up "yield from")
* Type checks
* Default values/optional arguments
* Varadic functions

You will also need to read code which I think will help you learn to
think in and use Python.

Links:
* https://docs.python.org/3.3/library/stdtypes.html#dict
* http://en.wikipedia.org/wiki/Binary_search_tree#Traversal
* https://docs.python.org/3.3/reference/expressions.html#yieldexpr

"""

from binarysearchtree import Node

class TreeDict(object):
    def __init__(self, *arg, **karg):
        self.node = Node()
        self.update(*arg, **karg)

    def update(self, *arg, **karg):

        for key, value in karg.items():
            if key == None:
                raise KeyError(key)
            else:
                self.node.insert(key,value)
        if len(arg)!= 0:
            if type(arg[0]).__name__ == "TreeDict":
                for ele in arg[0]:
                    self.node.insert(ele,arg[0][ele])
            elif isinstance(arg[0], dict):
                for key, value in arg[0].items():
                    if key == None:
                        raise KeyError(key)
                    else:
                        self.node.insert(key,value)
            elif hasattr(arg[0], '__iter__'):
                    for entry in arg[0]:
                        if len(entry) != 2:
                            raise ValueError(entry)
                        else:
                            if entry[0] == None:
                                raise KeyError(key)
                            else:
                                self.node.insert(entry[0],entry[1])

    def __getitem__(self, key):
        if key == None:
            raise KeyError(key)

        try:
            return self.node.lookup(key).value
        except ValueError:
            raise KeyError(key)


    def __setitem__(self, key, value):
        if key == None:
            raise KeyError(key)
        else:
            self.node.insert(key, value)


    def __contains__(self, key):
        if key == None:
            raise KeyError(key)
        try:
            if self.node.lookup(key).value != None:
                return True
        except ValueError:
            return False


    def get(self, key, default=None):
        if key == None:
            raise KeyError(key)
        try:
            return self.node.lookup(key).value
        except ValueError:
            return default


    def __delitem__(self, key):
        if key == None:
            raise KeyError(key)

        # self.node.delete(key)
        try:
            self.node.delete(key)
        except AttributeError:
            raise KeyError(key)


    def num_subtree_Nodes(self, root):
        if root == None:
            return 0
        else:
            return 1 + self.num_subtree_Nodes(root.left) + self.num_subtree_Nodes(root.right)

    def __len__(self):
        if self.node.key == None:
            return 0
        else:
            left_root = self.node.left
            right_root = self.node.right
            left_nodes_num = self.num_subtree_Nodes(left_root)
            right_nodes_num = self.num_subtree_Nodes(right_root)
            return left_nodes_num + right_nodes_num + 1

    def inOrder(self, root):
        if root != None:
            yield from self.inOrder(root.left)
            yield (root.key, root.value)
            yield from self.inOrder(root.right)

    def __iter__(self):
        return iter(()) if self.node.key == None else (item[0] for item in self.inOrder(self.node))

    def items(self):
        return iter({}) if self.node.key == None else (item for item in self.inOrder(self.node))

    def values(self):
        return iter(()) if self.node.key == None else (item[1] for item in self.inOrder(self.node))








