# The COPYRIGHT file at the top level of this repository contains the full i
# copyright notices and license terms.
from trytond.pool import PoolMeta


class Production(metaclass=PoolMeta):
    __name__ = 'production'

    @classmethod
    def _get_reschedule_planned_start_dates_domain(cls, date):
        domain = super()._get_reschedule_planned_start_dates_domain(date)

        new_state = ('state', 'in', ['assigned', 'waiting', 'draft'])
        for index, condition in enumerate(domain):
            if condition[0] == 'state':
                domain[index] = new_state
        return domain
