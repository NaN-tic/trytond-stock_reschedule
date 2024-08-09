import datetime as dt
import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = dt.date.today()

        # Activate modules
        activate_modules('stock_reschedule')

        # Create company
        _ = create_company()
        company = get_company()

        # Create customer
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()

        # Create product
        ProductUom = Model.get('product.uom')
        ProductTemplate = Model.get('product.template')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        template = ProductTemplate()
        template.name = 'Product'
        template.default_uom = unit
        template.type = 'goods'
        template.list_price = Decimal('20')
        template.save()
        product, = template.products

        # Get stock locations
        Location = Model.get('stock.location')
        warehouse_loc, = Location.find([('code', '=', 'WH')])
        customer_loc, = Location.find([('code', '=', 'CUS')])
        output_loc, = Location.find([('code', '=', 'OUT')])

        # Create Shipment Out
        ShipmentOutReturn = Model.get('stock.shipment.out.return')
        shipment_out_return = ShipmentOutReturn()
        shipment_out_return.planned_date = today
        shipment_out_return.customer = customer
        shipment_out_return.warehouse = warehouse_loc
        shipment_out_return.company = company

        # Add two shipment lines of same product
        StockMove = Model.get('stock.move')
        shipment_out_return.incoming_moves.extend([StockMove(), StockMove()])

        for move in shipment_out_return.incoming_moves:
            move.product = product
            move.uom = unit
            move.quantity = 1
            move.from_location = output_loc
            move.to_location = customer_loc
            move.company = company
            move.unit_price = Decimal('1')
            move.currency = company.currency

        shipment_out_return.save()

        # Reschedule shipment
        Cron = Model.get('ir.cron')
        cron = Cron(method='stock.shipment.out.return|reschedule')
        cron.interval_number = 1
        cron.interval_type = 'months'
        cron.click('run_once')
        shipment_out_return.reload()
        self.assertEqual(shipment_out_return.planned_date, today)
