'''
Created on Apr 16, 2025

@author: boogie
'''
from rkddr import block


MAGIC = 0x12345678.to_bytes(4, "little")


class Index(block.MappedBlock, block.Printable):
    offset = 0
    len = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 2, "offset", "len",
                 encoding="H", bitmasks=[(0, 8), (8, 8)])


class SdramInfov2(block.MappedBlock, block.Printable):
    version = 0
    cpu_gen = Index
    glob = Index
    ddr2 = Index
    ddr3 = Index
    ddr4 = Index
    ddr5 = Index
    lp2 = Index
    lp3 = Index
    lp4 = Index
    lp5 = Index
    skew = Index
    dqmap = Index
    lp4x = Index
    hash = Index

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 8, "magic", "version", encoding="4sI")
        self.addblock(cpu_gen=Index,
                      glob=Index,
                      ddr2=Index,
                      ddr3=Index,
                      ddr4=Index,
                      ddr5=Index,
                      lp2=Index,
                      lp3=Index,
                      lp4=Index,
                      lp5=Index,
                      skew=Index,
                      dqmap=Index,
                      lp4x=Index,
                      hash=Index,
                      )
