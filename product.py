# This file is part of the product_price_list_table module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import PYSONEncoder
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateAction, StateView, Button
from trytond.config import config as config_

__all__ = ['Template', 'ProductPriceListTableStart', 'ProductPriceListTable']

DIGITS = config_.getint('product', 'price_decimal', default=4)


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'
    price_qty1 = fields.Function(fields.Numeric('Price Quantity-1',
        digits=(16, DIGITS)), 'get_price_qty')
    price_qty2 = fields.Function(fields.Numeric('Price Quantity-2',
        digits=(16, DIGITS)), 'get_price_qty')
    price_qty3 = fields.Function(fields.Numeric('Price Quantity-3',
        digits=(16, DIGITS)), 'get_price_qty')
    price_qty4 = fields.Function(fields.Numeric('Price Quantity-4',
        digits=(16, DIGITS)), 'get_price_qty')
    price_qty5 = fields.Function(fields.Numeric('Price Quantity-5',
        digits=(16, DIGITS)), 'get_price_qty')

    @classmethod
    def get_price_qty(cls, templates, names):
        pool = Pool()
        PriceList = pool.get('product.price_list')
        Party = pool.get('party.party')
        Product = pool.get('product.product')
        context = Transaction().context
        products = [p for t in templates for p in t.products]
        result = {}
        for name in names:
            result[name] = {t.id: None for t in templates}
            if name in context and name in ('price_qty1', 'price_qty2',
                    'price_qty3', 'price_qty4', 'price_qty5'):
                qty = context[name]
                if qty:
                    price_list = PriceList(context['price_list'])
                    party = Party(context['party'])
                    prices = Product.get_sale_price(products, qty)
                    for template in templates:
                        if template.products:
                            product = template.products[0]
                        else:
                            continue
                        result[name][template.id] = price_list.compute(party,
                            product, prices[product.id], qty,
                            product.default_uom)
        return result


class ProductPriceListTableStart(ModelView):
    'Product Price List Table Start'
    __name__ = 'product.price.list.table.start'
    price_list = fields.Many2One('product.price_list', 'PriceList',
        required=True)
    party = fields.Many2One('party.party', 'Party')
    qty1 = fields.Integer('Quantity-1', required=True)
    qty2 = fields.Integer('Quantity-2')
    qty3 = fields.Integer('Quantity-3')
    qty4 = fields.Integer('Quantity-4')
    qty5 = fields.Integer('Quantity-5')


class ProductPriceListTable(Wizard):
    'Product Price List Table'
    __name__ = 'product.price.list.table'
    start = StateView('product.price.list.table.start',
        'product_price_list_table.product_price_list_table_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Ok', 'done', 'tryton-ok', True),
            ])
    done = StateAction(
        'product_price_list_table.action_product_price_list_table')

    def do_done(self, action):
        pool = Pool()
        Template = pool.get('product.template')

        templates = Template.browse(Transaction().context['active_ids'])
        products = [p for t in templates for p in t.products]

        action['pyson_domain'] = PYSONEncoder().encode([
                ('id', 'in', [p.id for p in products]),
                ])
        action['pyson_context'] = PYSONEncoder().encode({
                'price_list': self.start.price_list.id,
                'party': self.start.party and self.start.party.id or None,
                'price_qty1': self.start.qty1,
                'price_qty2': self.start.qty2,
                'price_qty3': self.start.qty3,
                'price_qty4': self.start.qty4,
                'price_qty5': self.start.qty5,
                })
        return action, {}

    def transition_done(self):
        return 'end'
