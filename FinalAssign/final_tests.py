from contextlib import contextmanager
import tempfile
import os
import unittest
import itertools
import re


import final

# You may find some of the functions or code here useful in either
# your tests or your implementation. Feel free to use it.

@contextmanager
def nonexistant_filename(suffix=""):
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as fi:
        filename = fi.name
    os.remove(filename)
    try:
        yield filename
    finally:
        os.remove(filename)

@contextmanager
def filled_filename(content, suffix=""):
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as fi:
        fi.write(content)
        filename = fi.name
    try:
        yield filename
    finally:
        os.remove(filename)

def windowed(iterable, size):
    window = list()
    for v in iterable:
        if len(window) < size:
            window.append(v)
        else:
            window.pop(0)
            window.append(v)
        if len(window) == size:
            yield window

def contains_sequence(iteratable, sequence, length=10000, require_length=True, times=1):
    sequence = list(sequence)
    count = 0
    found = 0
    for window in itertools.islice(windowed(iteratable, len(sequence)), length):
        #print(window, count, sequence)
        count += 1
        if window == sequence:
            found += 1
            if found >= times:
                return True
    if count < length-1 and require_length:
        raise AssertionError("Iterable did not contain enought values for check. Ran out at {}; needed {}.".format(count, length))
    return False


class RandomWriterTests(unittest.TestCase):
    """Some simple tests for RandomWriter.

    This is not an exhaustive test suite. You should write more.
    
    The entire set of tests should not take more than 2-3 seconds to
    run. My implementation takes 1.1s.
    """
    DEFAULT_LENGTH = 10000
    
    def assertContainsSequence(self, iteratable, sequence, length=None, times=1):
        length = length or self.DEFAULT_LENGTH
        self.assertTrue(contains_sequence(iteratable, sequence, length, times=times),
                        msg="The given iterable must contain the sequence: {} at least {} times "
                            "(in the first {} elements)".format(list(sequence), times, length))
    
    def assertNotContainsSequence(self, iteratable, sequence, length=None):
        length = length or self.DEFAULT_LENGTH
        self.assertFalse(contains_sequence(iteratable, sequence, length),
                         msg="The given iterable must NOT contain the sequence: {} "
                             "(in the first {} elements)".format(list(sequence), length))

    def test_numeric_sequence(self):
        rw = final.RandomWriter(2)
        rw.train_iterable((1,2,3,4,5,5,4,3,2,1))
        self.assertContainsSequence(rw.generate(), [3,4,5,5,4,3,2], times=100)
        self.assertNotContainsSequence(rw.generate(), [5,5,3])
        self.assertNotContainsSequence(rw.generate(), [1,2,5])

    def test_numeric_sequence1(self):
        rw = final.RandomWriter(2)
        rw.train_iterable((i for i in range(10)))
        self.assertContainsSequence(rw.generate(), [3,4,5,6,7,8,9], times=100)
        self.assertNotContainsSequence(rw.generate(), [5,5,3])
        self.assertNotContainsSequence(rw.generate(), [1,2,5])

    def test_numeric_sequence2(self):
        rw = final.RandomWriter(2)
        rw.train_iterable([1,2,3,4,5,5,4,3,2,1])
        self.assertContainsSequence(rw.generate(), [3,4,5,5,4,3,2], times=100)
        self.assertNotContainsSequence(rw.generate(), [5,5,3])
        self.assertNotContainsSequence(rw.generate(), [1,2,5])

    def test_characters(self):
        rw = final.RandomWriter(2, final.Tokenization.character)
        rw.train_iterable("abcdefghiab")
        self.assertContainsSequence(rw.generate(), "defghiabc", times=100)
        self.assertNotContainsSequence(rw.generate(), "ag")
        self.assertNotContainsSequence(rw.generate(), "ba")

    def test_characters1(self):
        rw = final.RandomWriter(2, final.Tokenization.none)
        rw.train_iterable((i for i in "abcdefghiab"))
        self.assertContainsSequence(rw.generate(), "defghiabc", times=100)
        self.assertNotContainsSequence(rw.generate(), "ag")
        self.assertNotContainsSequence(rw.generate(), "ba")

    def test_characters2(self):
        rw = final.RandomWriter(2, final.Tokenization.none)
        rw.train_iterable((i for i in "abcdefghiac"))
        self.assertContainsSequence(rw.generate(), "defghiac", times=100)
        self.assertNotContainsSequence(rw.generate(), "ag")
        self.assertNotContainsSequence(rw.generate(), "ba")

    def test_words(self):
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("the given iterable must contain the sequence the")
        self.assertContainsSequence(rw.generate(), "iterable must contain".split(" "), times=10)
        self.assertContainsSequence(rw.generate(), "the sequence".split(" "), times=200)
        self.assertNotContainsSequence(rw.generate(), "the the".split(" "))
        self.assertNotContainsSequence(rw.generate(), "the iterable".split(" "))

    def test_bytes(self):
        rw = final.RandomWriter(2, final.Tokenization.byte)
        rw.train_iterable(bytes("abcdefghiab",'ascii'))
        self.assertContainsSequence(rw.generate(), b"defghiabc", times=100)
        self.assertNotContainsSequence(rw.generate(), b"ag")
        self.assertNotContainsSequence(rw.generate(), b"ba")

    def test_generate_file1(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertContainsSequence(content, "abc", times=100)
            self.assertContainsSequence(content, "aeaeab", times=100)
            self.assertNotContainsSequence(content, "ac")
            self.assertNotContainsSequence(content, "aa")
            self.assertNotContainsSequence(content, "ce")

    def test_generate_file2(self):
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("a the word the")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertContainsSequence(content, "the word", times=100)
            self.assertNotContainsSequence(content, "the a")

    def test_generate_file3(self):
        rw = final.RandomWriter(2, final.Tokenization.none)
        rw.train_iterable((1,2,3,4,5,5,4,3,2,1))
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            #print(content)
            self.assertContainsSequence(content, "3 4 5 5 4 3 2", times=100)
            self.assertNotContainsSequence(content, "5 5 3")
            self.assertNotContainsSequence(content, "1 2 5")

    def test_generate_file4(self):
        rw = final.RandomWriter(1, final.Tokenization.byte)
        rw.train_iterable(bytes("abcaea",'utf-8'))
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rb") as fi:
                content = fi.read()
            self.assertContainsSequence(content, b"abc", times=100)
            self.assertContainsSequence(content, b"aeaeab", times=100)
            self.assertNotContainsSequence(content, b"ac")
            self.assertNotContainsSequence(content, b"aa")
            self.assertNotContainsSequence(content, b"ce")

    def test_url(self):
        rw = final.RandomWriter(2, final.Tokenization.word)
        rw.train_url("https://wordpress.org/plugins/about/readme.txt")
        self.assertContainsSequence(rw.generate(), "is the".split(" "), times=20)
        self.assertContainsSequence(rw.generate(), "if you".split(" "), times=10)
        self.assertNotContainsSequence(rw.generate(), "sdfsavg tdsafadsf".split(" "))
        self.assertNotContainsSequence(rw.generate(), "the the".split(" "))

    def test_save_text(self):
        line1_re = re.compile(r"\d+: \(\"b\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"a\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("aba")
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
            self.assertTrue(line1_re.match(line2) or line2_re.match(line2))
#
    def test_save_text_level2(self):
        line1_re = re.compile(r"\d+: \(\"b\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"a\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(2, final.Tokenization.character)
        rw.train_iterable("aba")
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1) or line1_re.match(line2) or line2_re.match(line2))

    def test_save_text(self):
        line1_re = re.compile(r"\d+: \(\"b\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"a\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("aba")
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
            self.assertTrue(line1_re.match(line2) or line2_re.match(line2))

    def test_save_text_word_mode(self):
        line1_re = re.compile(r"\d+: \(\"[0-9A-Za-z]+\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"[0-9A-Za-z]+\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("the given the")
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
            self.assertTrue(line1_re.match(line2) or line2_re.match(line2))

    def test_save_text_none_mode(self):
        line1_re = re.compile(r"\d+: \(\"[0-9A-Za-z]+\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"[0-9A-Za-z]+\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.none)
        rw.train_iterable((1,2,1))
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
            self.assertTrue(line1_re.match(line2) or line2_re.match(line2))

    def test_save_text_byte_mode(self):
        line1_re = re.compile(r"\d+: \(\"[0-9]+\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"[0-9]+\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.none)
        rw.train_iterable(bytes("aba",'ascii'))
        with nonexistant_filename() as fn:
            rw.save_text(fn)
            with open(fn, "rt") as fi:
                line1, line2 = fi.readlines()
            self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
            self.assertTrue(line1_re.match(line2) or line2_re.match(line2))

    def test_save_text_fileObj(self):
        line1_re = re.compile(r"\d+: \(\"b\",\s+1.0,\s+\d+\)")
        line2_re = re.compile(r"\d+: \(\"a\",\s+1.0,\s+\d+\)")

        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("aba")
        with open("fn.txt", "w") as fn:
            rw.save_text(fn)
        with open("fn.txt", "rt") as fi:
            line1, line2 = fi.readlines()
        self.assertTrue(line1_re.match(line1) or line2_re.match(line1))
        self.assertTrue(line1_re.match(line2) or line2_re.match(line2))

    def test_load_text(self):
        model_text = """\
1: ("2", 0.5, 2) ("3", 0.5, 3)
2: ("1", 1, 1)
3: ("1", 1, 1)
"""
        with filled_filename(model_text) as fn:
            rw = final.RandomWriter.load_text(fn)
            self.assertContainsSequence(rw.generate(), [1, 2, 1], times=100)
            self.assertContainsSequence(rw.generate(), [1, 3, 1], times=100)
            self.assertNotContainsSequence(rw.generate(), [1, 1])
            self.assertNotContainsSequence(rw.generate(), [2, 3])
            self.assertNotContainsSequence(rw.generate(), [3, 2])

    def test_load_text(self):
        model_text = """\
1: ("a", 0.5, 2) ("b", 0.5, 3)
2: ("c", 1, 1)
3: ("c", 1, 1)
"""
        with filled_filename(model_text) as fn:
            rw = final.RandomWriter.load_text(fn)
            self.assertContainsSequence(rw.generate(), "cac", times=100)
            self.assertContainsSequence(rw.generate(), "cbc", times=100)
            self.assertNotContainsSequence(rw.generate(), "cc")
            self.assertNotContainsSequence(rw.generate(), "ab")
            self.assertNotContainsSequence(rw.generate(), "ba")
#
    def test_save_load_pickle(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.save_pickle(fn)
            rw2 = final.RandomWriter.load_pickle(fn)
            self.assertContainsSequence(rw.generate(), "abc", times=100)
            self.assertContainsSequence(rw.generate(), "aeaeab", times=100)
            self.assertNotContainsSequence(rw.generate(), "ac")
            self.assertNotContainsSequence(rw.generate(), "aa")
            self.assertNotContainsSequence(rw.generate(), "ce")
#
    def test_load1(self):
        model_text = """\
1: ("2", 0.5, 2) ("3", 0.5, 3)
2: ("1", 1, 1)
3: ("1", 1, 1)
"""
        with filled_filename(model_text) as fn:
            rw = final.RandomWriter.load(fn)
            self.assertContainsSequence(rw.generate(), [1, 2, 1], times=100)
            self.assertContainsSequence(rw.generate(), [1, 3, 1], times=100)
            self.assertNotContainsSequence(rw.generate(), [1, 1])
            self.assertNotContainsSequence(rw.generate(), [2, 3])
            self.assertNotContainsSequence(rw.generate(), [3, 2])

    def test_load2(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.save_pickle(fn)
            rw2 = final.RandomWriter.load(fn)
            self.assertContainsSequence(rw.generate(), "abc", times=100)
            self.assertContainsSequence(rw.generate(), "aeaeab", times=100)
            self.assertNotContainsSequence(rw.generate(), "ac")
            self.assertNotContainsSequence(rw.generate(), "aa")
            self.assertNotContainsSequence(rw.generate(), "ce")

if __name__ == "__main__":
    unittest.main()

