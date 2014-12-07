"""A few very basic tests for CS105 Python Assignment 5.

This does not test for all the requirements of the assignment!

Run this script using:
python3.4 assignment5_test.py
It should work if you are in the same directory as your assignment5.py file.
If this does not work you may want to try:
PYTHONPATH=[directory containing assignment2.py] python3.4 assignment5_test.py
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

import unittest

import assignment5

class Assignment5Tests(unittest.TestCase):

    def check_constructor(self, cls, *args, **kws):
        self.assertIsInstance(cls, type)
        self.assertIsInstance(cls(*args, **kws), cls)

    def test_menu_init(self):
        self.check_constructor(assignment5.Menu)

    def test_order_init(self):
        self.check_constructor(assignment5.Order)

    def test_grouporder_init(self):
        self.check_constructor(assignment5.GroupOrder)

    def test_food_init(self):
        self.check_constructor(assignment5.Food, "Lasagna", 9.50)

    def test_drink_init(self):
        self.check_constructor(assignment5.Drink, "Lemonade", 1.50)

    def test_drink_attr(self):
        d = assignment5.Drink("Lemonade", 1.50)
        self.assertEqual(d.price, 1.50)

    def test_drink_prop(self):
        m = assignment5.Menu()
        d = assignment5.Drink("Lemonade", 1.50)
        m.add_item(d)
        self.assertEqual(d.price_plus_tax, 1.50 * 1.18)

    def test_menu_items(self):
        m = assignment5.Menu()
        d = assignment5.Drink("Lemonade", 1.50)
        f = assignment5.Food("Lasagna", 9.50)
        m.add_item(d)
        m.add_item(f)
        m.add_item(f)
        self.assertIs(d.menu, m)
        self.assertCountEqual(m.items, {d,f})
        self.assertTrue(m.items == {d,f})

    def test_order_items(self):
        m = object() # A mock object so this test can pass without a working Menu
        o = assignment5.Order()
        g = assignment5.GroupOrder()
        d = assignment5.Drink("Lemonade", 1.50)
        f = assignment5.Food("Toast", 0.75)
        dd = assignment5.Drink("Water", 0.50)
        d.menu = m
        dd.menu = m
        f.menu = object()
        self.assertTrue(o.add_item(d))
        self.assertTrue(o.add_item(d))
        self.assertTrue(o.add_item(dd))
        self.assertFalse(o.add_item(f))
        self.assertTrue(o.items == [d,d,dd])
        self.assertCountEqual(o.items, [d,d,dd])
        self.assertTrue(g.add_item(d))
        self.assertTrue(g.add_item(d))
        self.assertTrue(g.add_item(d))
        self.assertFalse(g.add_item(f))
        self.assertTrue(g.items == [d,d,d])
        self.assertCountEqual(g.items, [d,d,d])

    def test_order_price(self):
        m = assignment5.Menu()
        o = assignment5.Order()
        g = assignment5.GroupOrder()
        d = assignment5.Drink("Lemonade", 1.50)
        f = assignment5.Food("Toast", 0.75)
        d.menu = m
        f.menu = m
        o.add_item(d)
        o.add_item(f)
        g.add_item(d)
        g.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax, 1.50 * 1.18 + 0.75 * 1.10)
        self.assertAlmostEqual(o.price_plus_tax_and_tip(0.18), (1.50 * 1.18 + 0.75 * 1.10) * 1.18)
        self.assertAlmostEqual(g.price_plus_tax_and_tip(0.1), (1.50 * 1.18 + 0.75 * 1.10)*1.20)
        self.assertAlmostEqual(g.price_plus_tax_and_tip(0.15), (1.50 * 1.18 + 0.75 * 1.10)*1.20)
        self.assertAlmostEqual(g.price_plus_tax_and_tip(0.25), (1.50 * 1.18 + 0.75 * 1.10)*1.25)


if __name__ == "__main__":
    unittest.main()
