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
        yesterday = today - dt.timedelta(days=1)

        # Activate modules
        activate_modules('stock_reschedule')

        # Create company
        _ = create_company()
        company = get_company()

        # Create supplier
        Party = Model.get('party.party')
        supplier = Party(name='Supplier')
        supplier.save()

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
        storage_loc, = Location.find([('code', '=', 'STO')])
        supplier_loc, = Location.find([('code', '=', 'SUP')])
        warehouse_loc, = Location.find([('code', '=', 'WH')])

        # Create Shipment In
        ShipmentIn = Model.get('stock.shipment.in')
        shipment_in = ShipmentIn()
        shipment_in.planned_date = yesterday
        shipment_in.supplier = supplier
        shipment_in.warehouse = warehouse_loc
        move = shipment_in.moves.new()
        move.product = product
        move.unit = unit
        move.quantity = 1
        move.from_location = storage_loc
        move.to_location = supplier_loc
        move.company = company
        move.unit_price = Decimal('1')
        move.currency = company.currency
        shipment_in.save()
        self.assertEqual(shipment_in.state, 'draft')

        # Create incoming move
        StockMove = Model.get('stock.move')
        move_in = StockMove()
        move_in.planned_date = yesterday
        move_in.product = product
        move_in.unit = unit
        move_in.quantity = 2
        move_in.from_location = supplier_loc
        move_in.to_location = storage_loc
        move_in.unit_price = Decimal('1')
        move_in.currency = company.currency
        move_in.save()
        self.assertEqual(move_in.planned_date, yesterday)

        # Reschedule shipment
        Cron = Model.get('ir.cron')
        cron = Cron(method='stock.shipment.in|reschedule')
        cron.interval_number = 1
        cron.interval_type = 'months'
        cron.click('run_once')
        shipment_in.reload()
        self.assertEqual(shipment_in.planned_date, today)
        move_in.reload()
        self.assertEqual(move_in.planned_date, today)
