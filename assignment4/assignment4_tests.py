"""A few very basic tests for CS105 Python Assignment 4.

This does not test for all the requirements of the assignment!

Run this script using:
python3 assignment4_test.py
It should work if you are in the same directory as your assignment4.py file.
If this does not work you may want to try:
PYTHONPATH=[directory containing assignment2.py] python3 assignment4_test.py
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

from io import StringIO
from contextlib import contextmanager
import os
import tempfile
import time
import unittest
import sys

import assignment4

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class Assignment4Tests(unittest.TestCase):
    def test_has_exactly_type(self):
        self.assertTrue(assignment4.has_exactly_type(1, int))
        self.assertFalse(assignment4.has_exactly_type(True, int))
        self.assertTrue(assignment4.has_exactly_type(True, bool))

    def test_logcalls(self):
        @assignment4.logcalls("test")
        def f(arg):
            return arg + 1
        with captured_output() as (_, err):
            f(41)
            ls = err.getvalue().splitlines()
            self.assertIn("test: f(41)", ls)
            self.assertIn("test: f -> 42", ls)
        with captured_output() as (_, err):
            f(arg=41)
            self.assertIn("test: f(arg=41)", err.getvalue().splitlines())

    # def test_logcalls1(self):
    #     @assignment4.logcalls("test")
    #     def f(name, value, attri = "aa", spe = "bb"):
    #         return name + attri
    #     with captured_output() as (_, err):
    #         f("first",1,attri ="cc",spe="cc")
    #         ls = err.getvalue().splitlines()
    #         self.assertIn("test: f(\'first\',1,attri=\'cc\',spe=\'cc\')", ls)
    #         self.assertIn("test: f -> \'firstcc\'", ls)
    #
    # def test_logcalls2(self):
    #     @assignment4.logcalls("test")
    #     def f(list1, list2, list3 = [3], list4 = [4]):
    #         return list1 + list3
    #     with captured_output() as (_, err):
    #         f([1],[2],list3=[3],list4=[4])
    #         ls = err.getvalue().splitlines()
    #         self.assertIn("test: f([1],[2],list3=[3],list4=[4])", ls)
    #         self.assertIn("test: f -> [1, 3]", ls)

    def test_memoize(self):
        @assignment4.memoize
        def fib(n):
            if n > 1:
                return fib(n-1) + fib(n-2)
            else:
                return n
        self.assertEqual(fib.__name__, "fib")
        s = time.clock()
        self.assertEqual(fib(20), 6765)
        fib(100)
        e = time.clock()
        self.assertTrue(e - s < 1)

    def test_memoize1(self):
        @assignment4.memoize
        def fib(n = 2):
            if n > 1:
                return fib(n = n-1) + fib(n = n-2)
            else:
                return n
        self.assertEqual(fib.__name__, "fib")
        s = time.clock()
        self.assertEqual(fib(n=20), 6765)
        fib(n = 100)
        e = time.clock()
        self.assertTrue(e - s < 1)

    def test_memoize2(self):
        @assignment4.memoize
        def fib(m,n = 100):
            if m > 1 and n > 1:
                return fib(m-1,n=n-1) + fib(m-2,n=n-2)
            elif m > 1:
                return fib(m-1,n=n) + fib(m-2,n=n)
            elif n > 1:
                return fib(m,n=n-1) + fib(m,n=n-2)
            else:
                return m + n
        self.assertEqual(fib.__name__, "fib")
        s = time.clock()
        self.assertEqual(fib(20,n = 20), 13530)
        fib(100,n = 100)
        e = time.clock()
        self.assertTrue(e - s < 1)

    def test_memoize3(self):
        global next_num
        next_num = 0
        @assignment4.memoize
        def numbers(*args, **kws):
            global next_num
            next_num += 1
            return next_num
        self.assertEqual(numbers.__name__, "numbers")
        self.assertEqual(numbers(3,4,a=5), 1)
        self.assertEqual(numbers(3,4,a=5), 1)
        self.assertEqual(numbers(3,4,b=5), 2)
        self.assertEqual(numbers(3,4,b=5), 2)
        self.assertEqual(numbers(5,4,b=5), 3)

    def test_module_test(self):
        assignment4.module_test(assignment4)

        import assignment4_tests

        with captured_output() as (_, err):
            assignment4.module_test(assignment4)
            assignment4.module_test(assignment4_tests)
            ls = err.getvalue().splitlines()
            self.assertIn("test_has_exactly_type: PASS", ls)
            self.assertIn("test_false: FAIL", ls)
            self.assertIn("False Test Test", ls)
            self.assertIn("test_true: PASS", ls)
            self.assertIn("True Test Test", ls)

    def test_module_test1(self):
        with captured_output() as (_, err):
            assignment4.module_test(assignment4)
            ls = err.getvalue().splitlines()
            self.assertIn("test_has_exactly_type: PASS", ls)

            # self.assertIn("test_false: FAIL", ls)
            # self.assertIn("False Test Test", ls)
            # self.assertIn("test_true: PASS", ls)
            # self.assertIn("True Test Test", ls)

def test_false():
    "False Test Test"
    return False

def test_true():
    "True Test Test"
    return True
def test_empty():
    return True

if __name__ == "__main__":
    unittest.main()