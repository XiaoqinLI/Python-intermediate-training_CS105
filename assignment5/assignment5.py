"""
Assignment 5: Classes and objects

You will implement a set of classes that model a resturant menu.
"""


class Menu(object):
    """A menu of available items and some associated information.

    This class must have 2 class attributes drink_tax and food_tax that are
    used for the tax amount on drink and food. The value should be 0.18
    (18%) for drink, and 0.10 (10%) for food.
    """

    def __init__(self):
        self.drink_tax, self.food_tax = 0.18, 0.10
        self._items = set()

    def add_item(self, item):
        """Add an item to this menu and set it's menu attribute to this menu.

        Items should not be allowed to be added to more than one menu so check
        if the item is already in another menu.
        """
        if item.menu is None:
            self._items.add(item)
            item.menu = self
        else: pass

    # Add a read-only property named items that returns a copy
    # of the set of items in this menu
    @property
    def items(self):
        return set(self._items)


class Order(object):
    """A list of items that will be purchased together.

    This provides properties that compute prices with tax and tip for the whole
    order.
    """
    def __init__(self):
        self._items = []

    def add_item(self, item):
        """Add an item to this order.

        Items are required to all be part of one menu.

        Return True if the item was added, False otherwise (mainly if it was not
        part of the same menu as previous items).
        """
        if item.menu is not None:
            if len(self._items) == 0:
                self._items.append(item)
                return True
            else:
                if item.menu == self._items[0].menu:
                    self._items.append(item)
                    return True
                else:
                    return False
        else:
            return False

    @property
    def price_plus_tax(self):
        """A computed property that returns the sum of all the item prices
        including their tax."""
        sum_price = 0
        for ele in self._items:
            sum_price += ele.price_plus_tax
        return sum_price

    def price_plus_tax_and_tip(self, amount):
        """A method returns the sum of all the item prices with
        tax and a specified tip.

        amount is given as a propotion of the cost including tax.
        """
        return self.price_plus_tax * (1 + amount)

    # Add a read-only property named items that returns a copy
    # of the set of items in this order
    @property
    def items(self):
        return list(self._items)

class GroupOrder(Order):
    """An order than is made by a large ground and forces the tip to be at least
    20% (0.20).

    If a price with a tip less than 20% is requested return a price with a 20%
    tip instead.
    """

    #Override methods to force a tip of at least 20% (0.20). Do
    # not duplicate any code.
    def __init__(self):
        super().__init__()

    def price_plus_tax_and_tip(self, amount):
         return self.price_plus_tax * (1 + amount) if amount >= 0.2 else self.price_plus_tax * 1.2

    
class Item(object):
    """An item that can be baught.

    It has a name and a price attribute, and can compute it name with tax. This # name or price?
    also has a menu property that stores the menu this has been added to.
    """

    def __init__(self, name, price):
        self.name, self.price, self.menu = name, price, None

    @property
    def price_plus_tax(self):
        """Return the price of this item with tax added.

        Make sure you could support additional Item types. Other than what you
        have in this file. (Meaning isinstance checks will not work well.)
        """
        return self.price + self._applicable_tax

    @property
    def _applicable_tax(self):
        """Return the amount of tax applicable to this item."""
        # This is an abstract method. It should not be implemented in
        # this class.
        pass

# TODO: Implement 2 classes named Food and Drink that represent types
# of Items that can be on a menu (or in an order). They should each
# apply the correct amount of tax as specified by the menu they are
# associated with. You should not override price_plus_tax in these
# classes.

class Food(Item):
    def __init__(self, name, price):
        super().__init__(name, price)

    @property
    def _applicable_tax(self):
        return self.menu.food_tax * self.price


class Drink(Item):
    def __init__(self, name, price):
        super().__init__(name, price)

    @property
    def _applicable_tax(self):
        return self.menu.drink_tax * self.price




