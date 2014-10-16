# This file is part of the product_price_list_table module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .product import *

def register():
    Pool.register(
        Template,
        ProductPriceListTableStart,
        module='product_price_list_table', type_='model')
    Pool.register(
        ProductPriceListTable,
        module='product_price_list_table', type_='wizard')
