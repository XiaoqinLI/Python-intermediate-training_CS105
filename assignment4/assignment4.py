"""
Assignment 4: Metaprogramming

The idea of this assignment is to get you used to some of the dynamic
and functional features of Python and how they can be used to perform
useful metaprogramming tasks to make other development tasks easier.
"""

import functools
import logging
import sys


def has_exactly_type(obj, tpe):
    """Return true if obj has exactly type tpe.

    isinstance(obj, tpe) will always be true if has_exactly_type(obj,
    tpe) is true. However the converse is not true; isinstance(obj,
    tpe) may be true when has_exactly_type(obj, tpe) is false.

    This must work on all objects and types.
    """
    return type(obj) == tpe

def logcalls(prefix):
    """A function decorator that logs the arguments and return value
    of the function whenever it is called.

    The output should be to sys.stderr in the format:
    "{prefix}: {function name}({positional args}..., {keyword=args}, ...)"
    and
    "{prefix}: {function name} -> {return value}"
    respectively for call and return.

    Look up functools.wraps and use it to make the function you return
    have the same documentation and name as the function passed in.

    This will be used like:
    @logcalls("test")
    def f(arg):
        return arg

    (This is a more refined version of what I did in class)
    """
    # whitespace between arguments? __repr__
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            arg_all_str = ",".join([repr(arg) for arg in args] + [item[0] + "=" + repr(item[1])for item in kwargs.items()])
            sys.stderr.write(prefix + ": " + func.__name__ + "(" + arg_all_str + ")")
            sys.stderr.write("\n")
            sys.stderr.write(prefix + ": " + func.__name__ + " -> " + repr(func(*args, **kwargs)))
            return func(*args, **kwargs)
        return inner
    return decorator

def memoize(func):
    """A function decorator that memoizes a function.

    This should construct a local table and wrap the function with a
    lookup into the table and a store of the result if it needs to be
    computed. This should work with any function as long as it is only
    called with hashable arguments. Make sure you support any number
    of positional and keyword arguments.

    Do not use a global table.

    Use functools.wraps to make the function you return have the same
    documentation and name as the function passed in.

    This will be used like:
    @memoize
    def fib(n):
        if n > 1:
            return fib(n-1) + fib(n-2)
        else:
            return n

    There are implementations of this in the standard library. You
    should not use them or take any code from them at all.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def module_test(mod=None):
    """Run all the test functions in the module mod.

    The default value for the mod argument should be the module
    __main__, so that a user can write:
      if __name__ == '__main__':
          module_test()
    to easily test a module.

    A test function is a function with a name that begins with "test".
    You may assume that all the test functions take no arguments and
    return a value whose true-ness specifies whether the test
    succeeded (True) or failed (False). You do not have to worry about
    exceptions as we have not talked about them much yet.

    For each test, print a block to stderr (look up sys.stderr) in the
    following format:
      {test function name}: {either PASS or FAIL}
      {test function doc string}
    Make sure you correctly handle functions without doc strings.

    If you would like to you may support exceptions and use them in
    test_has_exactly_type.
    """
    func_list = [item[1] for item in mod.__dict__.items() if isinstance(item[0],str) and item[0].startswith('test')]
    sys.stderr.write("\n".join([func.__name__ + ": " + ("PASS" if func() else "FAIL") for func in func_list] + [ func.__doc__ for func in func_list if func.__doc__ is not None]))
    sys.stderr.write("\n")

def test_has_exactly_type():
    """A simple test of has_exactly_type.

    This should do a few basic checks to make sure has_exactly_type
    works. However really it is a test for module_test.
    """

    return has_exactly_type(1, int) and not has_exactly_type(True, int) and has_exactly_type(True, bool)
