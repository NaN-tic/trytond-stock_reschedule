# This file is part stock_reschedule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

def register():
    Pool.register(
        module='stock_reschedule', type_='model')
    Pool.register(
        module='stock_reschedule', type_='wizard')
    Pool.register(
        module='stock_reschedule', type_='report')
