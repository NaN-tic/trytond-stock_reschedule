# This file is part stock_reschedule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class StockRescheduleTestCase(ModuleTestCase):
    'Test Stock Reschedule module'
    module = 'stock_reschedule'
    extras = ['production']

    @with_transaction()
    def test_reschedule_domain(self):
        'Test reschedule domain'
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')
        ShipmentOutReturn = pool.get('stock.shipment.out.return')
        ShipmentIn = pool.get('stock.shipment.in')
        ShipmentInReturn = pool.get('stock.shipment.in.return')
        ShipmentInternal= pool.get('stock.shipment.internal')
        Production = pool.get('production')
        Date = pool.get('ir.date')

        today = Date.today()

        domain = ShipmentOut._get_reschedule_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], ['waiting', 'draft'])

        domain = ShipmentOutReturn._get_reschedule_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], ['waiting', 'draft'])

        domain = ShipmentIn._get_reschedule_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], 'draft')

        domain = ShipmentInReturn._get_reschedule_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], ['waiting', 'draft'])

        domain = ShipmentInternal._get_reschedule_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], ['waiting', 'draft'])

        domain = Production._get_reschedule_planned_start_dates_domain(date=today)
        state, = [condition for index, condition in enumerate(domain) if condition[0] == 'state']
        self.assertTrue(state[2], ['waiting', 'draft'])

del ModuleTestCase
