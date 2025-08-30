"""
 Copyright (C) 2025 boogie

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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


class Index16(block.MappedBlock, common.Printable):
    offset = 0
    len = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "offset", "len",
                 encoding="I", bitmasks=[(0, 16), (16, 8)])


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


class SdramInfov5(SdramInfov4):
    chan_pref = Index16
    com_pref = Index16

    def __init__(self, buffer, start=None):
        SdramInfov4.__init__(self, buffer, start=start)
        self._size += 2 + 4 * 2  # reserved 2 bytes 2 undefined prefs
        # self.addblock(chan_perf=Index16, com_perf=Index16)


class SdramInfov6(SdramInfov5):
    uartiomux = Index16

    def __init__(self, buffer, start=None):
        SdramInfov5.__init__(self, buffer, start=start)
        self.addblock(uartiomux=Index16)
