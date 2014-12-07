"""A few very basic tests for CS105 Python Assignment 6.

This does not test for all the requirements of the assignment!

Run this script using:
python3.4 assignment6_test.py
It should work if you are in the same directory as your assignment6.py file.
If this does not work you may want to try:
PYTHONPATH=[directory containing assignment2.py] python3.4 assignment6_test.py
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

import unittest
import itertools

import assignment6

shuffled_list = [39, 83, 31, 8, 66, 19, 45, 61, 86, 65, 28, 89, 95,
                 82, 40, 50, 88, 25, 47, 24, 51, 87, 93, 2, 67, 73, 7,
                 79, 98, 9, 34, 5, 72, 91, 64, 48, 30, 20, 37, 22, 43,
                 54, 46, 17, 55, 74, 49, 76, 35, 97, 14, 26, 10, 52,
                 78, 75, 13, 6, 4, 36, 77, 84, 59, 68, 11, 60, 71, 63,
                 0, 90, 57, 41, 70, 96, 15, 92, 21, 56, 38, 27, 53,
                 23, 18, 12, 16, 33, 85, 44, 69, 42, 1, 99, 32, 29,
                 81, 3, 80, 58, 94, 62]
shuffled_list2 = []

class Assignment6Tests(unittest.TestCase):

    def int_key_td(self):
        return assignment6.TreeDict((i, str(i)) for i in shuffled_list)
    def str_key_td(self):
        return assignment6.TreeDict({"one": 1, "two": 2})
    def int_key_td1(self):
        return assignment6.TreeDict([(101, '101'),(102, '102')])
    def int_key_td2(self):
        return assignment6.TreeDict((i, str(i)) for i in shuffled_list2)

    def test_construct(self):
        assignment6.TreeDict()
        assignment6.TreeDict((i, str(i)) for i in shuffled_list)
        assignment6.TreeDict((i, str(i)) for i in range(100))
        a = assignment6.TreeDict({'four': "1", 'five': "2"},one=1, two=2, three=3)
        for ele in a:
            print (ele)
        assignment6.TreeDict(one=1, two=2)
        assignment6.TreeDict(zip(['one', 'two', 'three'], [1, 2, 3]))

    def test_index(self):
        self.assertEqual(self.int_key_td()[50], "50")
        self.assertEqual(self.str_key_td()["one"], 1)
        self.assertNotEqual(self.int_key_td()[51], "50")
        # self.assertEqual(self.int_key_td()[101], None)  # need to double check

    def test_set(self):
        td = self.int_key_td()
        td[30] = 3
        td[1000] = 5
        self.assertEqual(td[30], 3)
        self.assertEqual(td[1000], 5)

    def test_in(self):
        td = self.int_key_td()
        self.assertIn(10, td)
        self.assertIn("two", self.str_key_td())
        # self.assertIn([3], td)
        self.assertNotIn(101, td)

    def test_get(self):
        self.assertEqual(self.int_key_td().get(50), "50")
        self.assertEqual(self.int_key_td().get(200), None)
        self.assertEqual(self.int_key_td().get(500), None)
        self.assertEqual(self.int_key_td().get(500, 400), 400)
        self.assertEqual(self.str_key_td().get("one"), 1)

    def test_del(self):
        td = self.int_key_td()
        del td[10]
        # del td[101]
        self.assertNotIn(10, td)

    def test_update1(self):
        td = self.int_key_td()
        td.update([(10, "ten"), (11, "eleven")])
        self.assertEqual(td[10], "ten")
        self.assertEqual(td[11], "eleven")
        td2 = self.int_key_td1()
        td.update(td2)
        self.assertEqual(td[101], '101')

    def test_update2(self):
        td = self.str_key_td()
        td.update(a="a", b=44, cccc=999)
        self.assertEqual(td["a"], "a")
        self.assertEqual(td["cccc"], 999)

    def test_len(self):
        self.assertEqual(len(self.int_key_td()), 100)
        self.assertEqual(len(self.str_key_td()), 2)
        self.assertEqual(len(assignment6.TreeDict()), 0)
        self.assertEqual(len(assignment6.TreeDict(one = 1)), 1)
        self.assertEqual(len(assignment6.TreeDict(one = 1, two = 2, three = 3)), 3)

    def test_iterate(self):
        self.assertEqual(list(self.int_key_td2()), list(range(0)))
        self.assertEqual(list(self.int_key_td()), list(range(100)))
        self.assertTrue(all(x == y
                            for x, y in itertools.zip_longest(self.int_key_td(), range(100))))

    def test_items(self):
        self.assertEqual(list(self.int_key_td2().items()), list(range(0)))
        self.assertEqual(list(self.int_key_td2().items()), [(y, str(y)) for y in range(0)])
        self.assertTrue(all(x == (y, str(y))
                            for x, y in itertools.zip_longest(self.int_key_td().items(), range(100))))

    def test_values(self):
        self.assertEqual(list(self.int_key_td2().values()), [str(y) for y in range(0)])
        self.assertEqual(list(self.int_key_td().values()), [str(y) for y in range(100)])
        self.assertTrue(all(x == str(y)
                            for x, y in itertools.zip_longest(self.int_key_td().values(), range(100))))

    def test_iterate2(self):
        self.assertEqual(list(self.str_key_td()), ["one", "two"])
        self.assertEqual(list(self.str_key_td().items()), [("one", 1), ("two", 2)])
        self.assertEqual(list(self.str_key_td().values()), [1, 2])
    #
    def test_raises_KeyError(self):
        td = self.str_key_td()
        with self.assertRaises(KeyError):
            td["aaaa"]

    def test_raises_on_None(self):
        try:
            td[None] = 1
            fail("This should throw an exception.")
        except:
            pass

if __name__ == "__main__":
    unittest.main()
