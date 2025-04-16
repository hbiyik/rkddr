'''
Created on Apr 16, 2025

@author: boogie
'''
from pyrkddr import block
from pyrkddr import common


MAGIC = 0x12345678.to_bytes(4, "little")


class Index(block.MappedBlock, common.Printable):
    offset = 0
    len = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 2, "offset", "len",
                 encoding="H", bitmasks=[(0, 8), (8, 8)])


class SdramInfov2(block.MappedBlock, common.Printable):
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
    dq = Index

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
                      dq=Index,
                      )

    def getblock(self, indexname, Block):
        if not hasattr(self, indexname):
            return
        index = getattr(self, indexname)
        if not index.len:
            return
        return Block(self._f, self.start + index.offset * 4)


class SdramInfov3(SdramInfov2):
    lp4x = Index
    lp4hash = Index

    def __init__(self, buffer, start=None):
        SdramInfov2.__init__(self, buffer, start=start)
        self.addblock(lp4x=Index, lp4hash=Index)


class SdramInfov4(SdramInfov3):
    lp5hash = Index
    ddr4hash = Index
    lp3hash = Index
    ddr3hash = Index
    lp2hash = Index
    ddr2hash = Index
    ddr5hash = Index

    def __init__(self, buffer, start=None):
        SdramInfov3.__init__(self, buffer, start=start)
        self.addblock(lp5hash=Index,
                      ddr4hash=Index,
                      lp3hash=Index,
                      ddr3hash=Index,
                      lp2hash=Index,
                      ddr2hash=Index,
                      ddr5hash=Index,
                      )
