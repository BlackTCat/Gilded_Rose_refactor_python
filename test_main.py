import unittest
from main import *

class maintest(unittest.TestCase):

    def test_new_item_default_quality(self):
        item = NewItem("Default item", 10, 40, Store.calc_method_quality_default)
        item.update_quality()
        expected_values = (9, 39)
        self.assertEqual(expected_values, (item.sell_in, item.quality))

    def test_new_item_sulfuras(self):
        item = NewItem("Sulfuras", 10, 80, Store.calc_method_quality_stable)
        for i in range(10):
            item.update_quality()

        expected_values = (10, 80)
        self.assertEqual(expected_values, (item.sell_in, item.quality))
