"""An implementation of a binary search tree.

Read and understand this code. This is part of the assignment so don't
ask for outside help with this specific code or discuss this code with
class mates, however feel free to look things up or discuss general
concepts to help you understand what you are reading.

You may find it useful to add comments and documentation to this file
as you go. However do not change the code in this module in any
substantial way. I will be testing with my own version.

NOTE: This code is intentionally uncommented to force you to read and
understand it. However it is not obfuscated in any way. That being
said if you were to write something like this you should comment
it. It does need comments to make it easier to work with.

"""

class Node(object):
    __slots__ = ("left", "right", "key", "value")
    
    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value

    @classmethod
    def _insert_in_child(cls, child, key, value):
        if child:
            return child, child.insert(key, value)
        else:
            node = cls(key, value)
            return node, node

    def insert(self, key, value):
        if key is None:
            raise ValueError("None cannot be used as a key")
        if self.key is not None:
            if key < self.key:
                self.left, ret = self._insert_in_child(self.left, key, value)
            elif key > self.key:
                self.right, ret = self._insert_in_child(self.right, key, value)
            else:
                self.value = value
                ret = self
            return ret   # after insert, you still return this node just created??
        else:
            self.key = key
            self.value = value
            return self  # after insert, you still return this node just created??

    @staticmethod
    def _lookup_in_child(child, key):
        if child:
            return child.lookup(key)
        else:
            raise ValueError("Key not in tree: " + repr(key)) 

    def lookup(self, key):
        if key is None:
            raise ValueError("None cannot be used as a key")
        if self.key is None:
            raise ValueError("Key not in tree: " + repr(key))

        if key < self.key:
            return self._lookup_in_child(self.left, key)
        elif key > self.key:
            return self._lookup_in_child(self.right, key)
        else:
            return self

    def _delete_internal(self, key, parent):
        if key < self.key:
            self.left._delete_internal(key, self)
        elif key > self.key:
            self.right._delete_internal(key, self)
        else:
            if self.left and self.right:
                n, parent = self._next_descendant()
                self.key, self.value = n.key, n.value
                n._delete_internal(n.key, parent)
            elif self.left or self.right:
                child = self.left or self.right
                self.key, self.value = child.key, child.value
                self.left, self.right = child.left, child.right
            else:
                if parent:
                    if parent.left is self:
                        parent.left = None
                    elif parent.right is self:
                        parent.right = None
                    else:
                        raise RuntimeError("Bug in BST implementation: parent "
                                           "does not have self as a child")
                else:
                    self.key = None
                    self.value = None

    def delete(self, key):
        if key is None:
            raise ValueError("None cannot be used as a key")
        self._delete_internal(key, None)

    def _next_descendant(self):
        parent = self
        n = self.right
        if not n:
            return None, parent
        while n.left:
            parent, n = n, n.left
        return n, parent

    def min_child(self):
        n = self.left
        if not n:
            return self
        while n.left:
            n = n.left
        return n
