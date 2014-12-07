"""A few very basic tests for CS105 Python Assignment 2.

This does not test for all the requirements of the assignment!

Run this script using:
python3 assignment2_test.py
It should work if you are in the same directory as your assignment2.py file.
If this does not work you may want to try:
PYTHONPATH=[directory containing assignment2.py] python3 assignment2_test.py
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code work with this exact version.

import unittest

import assignment2

class Assignment2Tests(unittest.TestCase):
    def test_linear_fib(self):
        self.assertEqual(assignment2.linear_fib(2), 1)
    def test_linear_fib1(self):
        self.assertEqual(assignment2.linear_fib(0), 0)
    def test_linear_fib2(self):
        self.assertEqual(assignment2.linear_fib(1), 1)
    def test_linear_fib3(self):
        self.assertEqual(assignment2.linear_fib(20), 6765)

    def test_flip_dict(self):
        self.assertEqual(assignment2.flip_dict({2: 10}), {10: 2})
    def test_flip_dict1(self):
        self.assertEqual(assignment2.flip_dict({2: 8, 8: (2,3,4), (2,3):(1,3,5)}), {8: 2, (1, 3, 5): (2, 3), (2, 3, 4): 8})
    def test_flip_dict2(self):
        self.assertEqual(assignment2.flip_dict({}), {})

    def test_remove_duplicates(self):
        self.assertEqual(set(assignment2.remove_duplicates((1,(2,3),(3,2),2,3,(2,3),2,3))), set([1,(2,3),(3,2),2,3]))
    def test_remove_duplicates1(self):
        self.assertEqual(set(assignment2.remove_duplicates((2,4,2,3,2,5))), set([2,4,3,5]))
    def test_remove_duplicates10(self):
        self.assertEqual(assignment2.remove_duplicates((2,4,2,3,2,5)), [2,4,3,5])
    def test_remove_duplicates2(self):
        self.assertEqual(set(assignment2.remove_duplicates(('a','b','a','c'))), set(['a','b','c']))
    def test_remove_duplicates3(self):
        self.assertEqual(set(assignment2.remove_duplicates(())), set([]))
    def test_remove_duplicates4(self):
        self.assertEqual(set(assignment2.remove_duplicates("baacadbe")), set(['b','a','c','d','e']))
    def test_remove_duplicates5(self):
        self.assertEqual(set(assignment2.remove_duplicates([2,1,frozenset([3,2,3,1,4]),3,frozenset([4,3,2,3,1]),2,])), set([2,1,frozenset([1,2,2,3,4]),3]))
    def test_remove_duplicates6(self):
        self.assertEqual(set(assignment2.remove_duplicates(["abc","cba","dhe","abc"])), set(["abc","cba","dhe","abc"]))

    def test_remove_duplicates_unhashable(self):
        self.assertEqual(assignment2.remove_duplicates_unhashable([{3:4,1:2},{2:1,4:3},{3:4,1:2}]), [{3:4,1:2},{2:1,4:3}])
    def test_remove_duplicates_unhashable1(self):
        self.assertEqual(assignment2.remove_duplicates_unhashable([[3,2],{3:4,1:2},[1,2],{2:1,4:3},[3,2],{3:4,1:2}]), [[3,2],{1:2,3:4},[2,1],{2:1,4:3}])
    def test_remove_duplicates_unhashable1(self):
        self.assertNotEqual(set(assignment2.remove_duplicates_unhashable([1,{(1,2),(1,2),3}, {3,(1,2)},3])), [1,set({(1, 2), 3}), 3])

    def test_generate_unique_id(self):
        self.assertEqual(assignment2.generate_unique_id(1000), assignment2.generate_unique_id(1000))
        self.assertNotEqual(assignment2.generate_unique_id(1000), assignment2.generate_unique_id(1001))
        self.assertEqual(assignment2.generate_unique_id([1,2,3]), assignment2.generate_unique_id([1,2,3]))
        self.assertNotEqual(assignment2.generate_unique_id([1,2,3]), assignment2.generate_unique_id([3,2,1]))
        self.assertNotEqual(assignment2.generate_unique_id([1,2,3]), assignment2.generate_unique_id([1,2,4]))
        self.assertEqual(assignment2.generate_unique_id((1,2,3)), assignment2.generate_unique_id((1,2,3)))
        self.assertNotEqual(assignment2.generate_unique_id((1,2,3)), assignment2.generate_unique_id((3,2,1)))
        self.assertEqual(assignment2.generate_unique_id({1:2,3:4}), assignment2.generate_unique_id({3:4,1:2}))
        self.assertNotEqual(assignment2.generate_unique_id({1:2,3:4}), assignment2.generate_unique_id({3:2,1:4}))
        self.assertEqual(assignment2.generate_unique_id({1,2,3,2}), assignment2.generate_unique_id({1,2,2,3}))
        self.assertNotEqual(assignment2.generate_unique_id({1,2,3}), assignment2.generate_unique_id({1,3,4}))

    def test_union(self):
        self.assertEqual(set(assignment2.union([1,3,4], frozenset([2,3,4]))),set([1,2,3,4]))
    def test_union1(self):
        self.assertEqual(set(assignment2.union("China","America")), set("China")|set("America"))
    def test_union2(self):
        self.assertEqual(set(assignment2.union("China",[1,3,2,2,3,4])), set("China")|set([1,2,3,4]))


if __name__ == "__main__":
    unittest.main()
