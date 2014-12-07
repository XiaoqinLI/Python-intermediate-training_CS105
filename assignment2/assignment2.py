"""
Implement each function as described in it's doc string.

Use any or all of the data structures in class and also look for
functions that might useful in the standard library.

For all of these remember that None is a valid value.

Make sure to use descriptive names for variables.
"""

import sys
import collections
from collections import Iterable
assert sys.version_info.major == 3

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(self.items()))

class hashablelist(list):
    def __hash__(self):
        return hash(tuple(self))

class hashableset(set):
    def __hash__(self):
        return hash(tuple(self))

cache = {}
def linear_fib(n):
    """Compute fib(n) in O(n) time using memoization.

    Use a global variable and one of the data structures you have
    learned about to implement a linear time recursive Fibonacci. Use
    memoization; it is possible to implement Fibonacci in linear time
    without memoization (using a loop), but that is not the
    assignment.
    """
    global cashe
    if n < 0:
        return None
    elif n == 0 or n == 1:
        cache[n] = n
        return n
    else:
        if n in cache:
            return cache[n]
        else:
            cache[n] = linear_fib(n-1) + linear_fib(n-2)
            return cache[n]

def flip_dict(d):
    """Return a dict that has the values of d as keys and the keys of
    d as values.

    So given input {2: 10} it should return {10: 2}. You may assume
    that the input does not have duplicate values.
    """
    reversed_dict = {}
    for key, value in d.items():
        reversed_dict[value] = key
    return reversed_dict

def remove_duplicates(l):
    """Given an iterable, return a list that has no duplicates.

    The result should keep the first (in traversal order) of the
    duplicates and maintain the order of the elements.

    You may assume all the elements in the argument are hashable.

    Your implementation must be better than O(n^2) (on average).
    """
    checkSet = set()
    results = []
    for entry in l:
        if entry not in checkSet:
            checkSet.add(entry)
            results.append(entry)
    return results

def remove_duplicates_unhashable(l):
    """Given an iterable, return a list that has no duplicates.

    The result should keep the first (in traversal order) of the
    duplicates and maintain the order of the elements.

    This is the same as remove_duplicates above however, you may NOT
    assume all the elements in the argument are hashable. This
    implementation will be slower than the one that assumes
    hashability.
    """
    checkSet = set()
    results = []
    for entry in l:
        if isinstance(entry, collections.Hashable):
            if entry not in checkSet:
                checkSet.add(entry)
                results.append(entry)
        else:
            if isinstance(entry,dict):
                entry = hashabledict(entry)
            elif isinstance(entry,list):
                entry = hashablelist(entry)
            elif isinstance(entry,set):
                entry = hashableset(entry)

            if entry not in results:
                checkSet.add(entry)
                results.append(entry)
    return list(results)

autoUniqueID = 0
hashTable = {}
def generate_unique_id(obj):
    """Return a "small" unique number for each object passed in.

    The first time an object is passed in it should be assigned a
    number. Then if it is passed in again this function should return
    the same number. By a small number I mean a number that is no
    larger than the number of objects that have ever been passed to
    this function.

    Formally:
      If a == b then generate_unique_id(a) == generate_unique_id(b)
      and
      if a != b then generate_unique_id(a) != generate_unique_id(b)

    You may assume all objects passed in will not be mutated. However
    you need to support lists and dicts in addition to hashable
    objects.
    """
    global autoUniqueID
    global hashTable

    if  isinstance(obj, collections.Hashable):
        if obj in hashTable.keys():
            return hashTable[obj]
        else:
            hashTable[obj] = autoUniqueID
            autoUniqueID += 1
            return hashTable[obj]
    else:
        if isinstance(obj,dict):
            obj = hashabledict(obj)
        elif isinstance(obj,list):
            obj = hashablelist(obj)
        elif isinstance(obj,set):
            obj = hashableset(obj)

        if obj in hashTable.keys():
            return hashTable[obj]
        else:
            hashTable[obj] = autoUniqueID
            autoUniqueID += 1
            return hashTable[obj]

def union(x, y):

    """Return the union of x and y when they are viewed as sets.

    Do not create any unnecessary copies. You may assume that any
    union method does what you expect it to. Remember union is
    commutative.

    The returned value should be a set like object regardless of the
    input parameters. For this assignment take set-line to mean an
    object with a union method.
    """
    if not (isinstance(x,set) or isinstance(x,frozenset)):
       x = set(x)
    if not (isinstance(y,set) or isinstance(y,frozenset)):
       y = set(y)
    return x | y

