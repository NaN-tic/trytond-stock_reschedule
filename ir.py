# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta


class Cron(metaclass=PoolMeta):
    __name__ = 'ir.cron'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.method.selection.extend([
                ('stock.shipment.out.return|reschedule',
                    "Reschedule Out Return Shipments"),
                ('stock.shipment.in|reschedule',
                    "Reschedule In Shipments"),
                ])
