# This file is part of the product_price_list_table module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.Template,
        product.ProductPriceListTableStart,
        module='product_price_list_table', type_='model')
    Pool.register(
        product.ProductPriceListTable,
        module='product_price_list_table', type_='wizard')
