'''
Created on Apr 16, 2025

@author: boogie
'''
from pyrkddr import block
from pyrkddr import common


class Mask(block.MappedBlock, common.Printable):
    channelmask = 0
    bankmask0 = 0
    bankmask1 = 0
    rankmask = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 8 * 4, "channelmask", "bankmask0", "bankmask1", "rankmask0", encoding="QQQQ")
