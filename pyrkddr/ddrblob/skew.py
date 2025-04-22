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


class Base(block.MappedBlock, common.Printable):
    ca0 = 0
    ca1 = 0
    ca2 = 0
    ca3 = 0
    ca4 = 0
    ca5 = 0
    ca6 = 0
    ca7 = 0
    ca8 = 0
    ca9 = 0
    ca10 = 0
    ca11 = 0
    ca12 = 0
    ca13 = 0
    ca14 = 0
    ca15 = 0
    ras = 0
    cas = 0
    ba0 = 0
    ba1 = 0
    ba2 = 0
    we = 0
    cke0 = 0
    cke1 = 0
    ckn = 0
    ckp = 0
    odt0 = 0
    odt1 = 0
    cs0 = 0
    cs1 = 0
    resetn = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "ca1", "ca13", "ca14", "ca9", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "ca6", "ca3", "ca4", "ca2", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "ca7", "ca0", "ca11", "ca5", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "ba1", "odt0", "ca8", "ca10", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "ca12", "ba2", "cke0", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (24, 8)])
        self.map(0, 4, "cke1", "ras", "ca15", "ba0", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "odt1", "we", "ckp", "ckn", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "cs0", "resetn", "cs1", "cas", encoding="I",
                 bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])


class Skew(block.MappedBlock, common.Printable):
    subversion = 0
    ddr3 = Base
    ddr4 = Base
    lp3 = Base

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "subversion", encoding="I")
        self.addblock(ddr3=Base, ddr4=Base, lp3=Base)
