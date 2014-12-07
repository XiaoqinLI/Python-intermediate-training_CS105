"""A few very basic tests for CS105 Python Assignment 3.

This does not test for all the requirements of the assignment!

Run this script using:
python3 assignment3_test.py
It should work if you are in the same directory as your assignment3.py file.
If this does not work you may want to try:
PYTHONPATH=[directory containing assignment2.py] python3 assignment3_test.py
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code work with this exact version.

from contextlib import contextmanager
import csv
import os
import tempfile
import unittest

import assignment3


@contextmanager
def filled_filename(content, suffix=""): # creating a virtual csv
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, encoding="utf-8",delete=False) as fi:
        fi.write(content)
        filename = fi.name
    try:
        yield filename
    finally:
        os.remove(filename)

class Assignment3Tests(unittest.TestCase):
        
    def test_read_csv(self):
        with filled_filename("1,2,3\n4,5\n", suffix=".csv") as fn:
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "2", "3"), ("4", "5")])

    def test_read_csv1(self):
        with filled_filename("1, 2,3\n4,  5\n", suffix=".csv") as fn:
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", " 2", "3"), ("4", "  5")])

    def test_read_csv2(self):
        with filled_filename("1,2,3\n4,中国\n", suffix=".csv") as fn:
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "2", "3"), ("4", "中国")])

    def test_read_csv3(self):
        with filled_filename("1,2,3\n4, 穫\n", suffix=".csv") as fn:
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "2", "3"), ("4", " 穫")])

    def test_write_csv(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "2", "3"), (4, 5)], False)
            with open(fn, "r", newline="", encoding="utf-8") as fi:
                reader = csv.reader(fi)
                self.assertEqual([tuple(r) for r in reader], [("1", "2", "3"), ("4", "5")])

    def test_write_csv1(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "  2", "中 "), (4, " 国")], False)
            with open(fn, "r", newline="",encoding="utf-8") as fi:
                reader = csv.reader(fi)
                self.assertEqual([tuple(r) for r in reader], [("1", "  2", "中 "), ("4", " 国")])

    def test_write_read_csv(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "2", "3"), (4, 5)], False)
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "2", "3"), ("4", "5")])

    def test_write_read_csv1(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "  2", "中 "), (4, " 国")], False)
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "  2", "中 "), ("4", " 国")])

    def test_write_read_csv_compressed(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "2", "3"), (4, 5)], True)
            # Really ought to check if it really is compressed.
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "2", "3"), ("4", "5")])

    def test_write_read_csv_compressed1(self):
        with filled_filename("", suffix=".csv") as fn:
            assignment3.write_csv(fn, [("1", "  2", "中  "), (4, '国')], True)
            # Really ought to check if it really is compressed.
            self.assertEqual(list(assignment3.read_csv(fn)), [("1", "  2", "中  "), ("4", "国")])

    def test_to_int(self):
        self.assertEqual(list(assignment3.tuples_to_int_tuples([("1", "2", 3), ("4", "5")])),
                         [(1, 2, 3), (4, 5)])
    def test_to_int1(self):
        self.assertEqual(list(assignment3.tuples_to_int_tuples([("1", "0xff", 3), ("0xe", "5")])),
                         [(1, 255, 3), (14, 5)])

    def test_totals(self):
        self.assertEqual(list(assignment3.compute_totals([(1, 2, 3), (4, 5)])),
                         [(6, 1, 2, 3),
                          (9, 4, 5),
                          (15, 5, 7, 3)])

    def test_totals1(self):
        self.assertEqual(list(assignment3.compute_totals([(1, 6, 2, 4), (3, 8, 5, 4, 0, 1, 2), (2, 5)])),
                         [(13, 1, 6, 2, 4),
                          (23, 3, 8, 5, 4, 0, 1, 2),
                          (7, 2, 5),
                          (43, 6, 19, 7, 8, 0, 1, 2)])

if __name__ == "__main__":
    unittest.main()
