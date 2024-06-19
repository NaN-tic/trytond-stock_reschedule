# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


class ShipmentInternal(metaclass=PoolMeta):
    __name__ = 'stock.shipment.internal'

    @classmethod
    def _get_reschedule_domain(cls, date):
        domain = super()._get_reschedule_domain(date)

        new_state = ('state', 'in', ['assigned', 'waiting', 'draft'])
        for index, condition in enumerate(domain):
            if condition[0] == 'state':
                domain[index] = new_state
        return domain


class ShipmentIn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    @classmethod
    def _get_reschedule_domain(cls, date):
        return [
            ('state', '=', 'draft'),
            ('planned_date', '<', date),
            ]

    @classmethod
    def _get_reschedule_incoming_move_domain(cls, date):
        return [
            ('state', '=', 'draft'),
            ('planned_date', '<', date),
            ('from_location.type', '=', 'supplier'),
            ('shipment', '=', None),
            ]

    @classmethod
    def reschedule(cls, date=None):
        pool = Pool()
        Date = pool.get('ir.date')
        Move = pool.get('stock.move')

        if date is None:
            date = Date.today()
        shipments = cls.search(cls._get_reschedule_domain(date))
        cls.write(shipments, {'planned_date': date})

        moves = Move.search(cls._get_reschedule_incoming_move_domain(date))
        Move.write(moves, {'planned_date': date})


class ShipmentInReturn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in.return'

    @classmethod
    def _get_reschedule_domain(cls, date):
        domain = super()._get_reschedule_domain(date)

        new_state = ('state', 'in', ['assigned', 'waiting', 'draft'])
        for index, condition in enumerate(domain):
            if condition[0] == 'state':
                domain[index] = new_state
        return domain


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @classmethod
    def _get_reschedule_domain(cls, date):
        domain = super()._get_reschedule_domain(date)

        new_state = ('state', 'in', ['assigned', 'waiting', 'draft'])
        for index, condition in enumerate(domain):
            if condition[0] == 'state':
                domain[index] = new_state
        return domain


class ShipmentOutReturn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'

    @classmethod
    def _get_reschedule_domain(cls, date):
        return [
            ('state', 'in', ['waiting', 'draft']),
            ('planned_date', '<', date),
            ]

    @classmethod
    def reschedule(cls, date=None):
        pool = Pool()
        Date = pool.get('ir.date')
        if date is None:
            date = Date.today()
        shipments = cls.search(cls._get_reschedule_domain(date))
        cls.write(shipments, {'planned_date': date})
