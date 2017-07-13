"""
irqbalance_conf - File ``/etc/sysconfig/irqbalance``
====================================================

Share parser for parsing file ``/etc/sysconfig/irqbalance``.
"""

from .. import Parser, parser, LegacyItemAccess
from ..parsers import split_kv_pairs


@parser('sysconfig_irqbalance')
class SysconfigIrqbalance(LegacyItemAccess, Parser):
    """
    A parser for analyzing the ``irqbalance`` service config file in the
    ``/etc/sysconfig`` directory.

    Sample Input::

        #IRQBALANCE_ONESHOT=yes
        #
        # IRQBALANCE_BANNED_CPUS
        # 64 bit bitmask which allows you to indicate which cpu's should
        # be skipped when reblancing irqs. Cpu numbers which have their
        # corresponding bits set to one in this mask will not have any
        # irq's assigned to them on rebalance
        #
        IRQBALANCE_BANNED_CPUS=f8

        IRQBALANCE_ARGS="-d"

    Examples:

        >>> irqb_syscfg = shared[SysconfigIrqbalance]
        >>> irqb_syscfg['IRQBALANCE_BANNED_CPUS']
        'f8'
        >>> irqb_syscfg.get('IRQBALANCE_ARGS')
        '"-d"'
        >>> irqb_syscfg.get('IRQBALANCE_ONESHOT')
        None
        >>> 'ONESHOT' in irqb_syscfg
        False

    """
    def parse_content(self, content):
        self.data = split_kv_pairs(content)