# This file is part stock_reschedule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import ir
from . import shipment
from . import production

def register():
    Pool.register(
        ir.Cron,
        shipment.ShipmentIn,
        shipment.ShipmentInReturn,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        shipment.ShipmentInternal,
        module='stock_reschedule', type_='model')
    Pool.register(
        production.Production,
        module='stock_reschedule', type_='model',
        depends=['production'])
