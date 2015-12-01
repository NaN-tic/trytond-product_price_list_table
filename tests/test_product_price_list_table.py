# This file is part of the product_price_list_table module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductPriceListTableTestCase(ModuleTestCase):
    'Test Product Price List Table module'
    module = 'product_price_list_table'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListTableTestCase))
    return suite