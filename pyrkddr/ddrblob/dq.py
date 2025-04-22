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


class Map(block.MappedBlock, common.Printable):
    ddr4 = 0
    ddr2 = 0
    ddr3 = 0
    lp2 = 0
    lp3 = 0
    lp4 = 0
    lp3_dq0 = 0
    lp3_dq1 = 0
    lp3_dq2 = 0
    lp3_dq3 = 0
    lp3_dq4 = 0
    lp3_dq5 = 0
    lp3_dq6 = 0
    lp3_dq7 = 0
    lp2_dq0 = 0
    lp2_dq1 = 0
    lp2_dq2 = 0
    lp2_dq3 = 0
    lp2_dq4 = 0
    lp2_dq5 = 0
    lp2_dq6 = 0
    lp2_dq7 = 0
    ddr4_cs0_dq0 = 0
    ddr4_cs0_dq1 = 0
    ddr4_cs0_dq2 = 0
    ddr4_cs0_dq3 = 0
    ddr4_cs0_dq5 = 0
    ddr4_cs0_dq6 = 0
    ddr4_cs0_dq7 = 0
    ddr4_cs0_dq8 = 0
    ddr4_cs0_dq9 = 0
    ddr4_cs0_dq10 = 0
    ddr4_cs0_dq11 = 0
    ddr4_cs0_dq12 = 0
    ddr4_cs0_dq13 = 0
    ddr4_cs0_dq14 = 0
    ddr4_cs0_dq15 = 0
    ddr4_cs0_dq16 = 0
    ddr4_cs0_dq17 = 0
    ddr4_cs0_dq18 = 0
    ddr4_cs0_dq19 = 0
    ddr4_cs0_dq20 = 0
    ddr4_cs0_dq21 = 0
    ddr4_cs0_dq22 = 0
    ddr4_cs0_dq23 = 0
    ddr4_cs0_dq24 = 0
    ddr4_cs0_dq25 = 0
    ddr4_cs0_dq26 = 0
    ddr4_cs0_dq27 = 0
    ddr4_cs0_dq28 = 0
    ddr4_cs0_dq29 = 0
    ddr4_cs0_dq30 = 0
    ddr4_cs0_dq31 = 0
    ddr4_cs1_dq0 = 0
    ddr4_cs1_dq1 = 0
    ddr4_cs1_dq2 = 0
    ddr4_cs1_dq3 = 0
    ddr4_cs1_dq5 = 0
    ddr4_cs1_dq6 = 0
    ddr4_cs1_dq7 = 0
    ddr4_cs1_dq8 = 0
    ddr4_cs1_dq9 = 0
    ddr4_cs1_dq10 = 0
    ddr4_cs1_dq11 = 0
    ddr4_cs1_dq12 = 0
    ddr4_cs1_dq13 = 0
    ddr4_cs1_dq14 = 0
    ddr4_cs1_dq15 = 0
    ddr4_cs1_dq16 = 0
    ddr4_cs1_dq17 = 0
    ddr4_cs1_dq18 = 0
    ddr4_cs1_dq19 = 0
    ddr4_cs1_dq20 = 0
    ddr4_cs1_dq21 = 0
    ddr4_cs1_dq22 = 0
    ddr4_cs1_dq23 = 0
    ddr4_cs1_dq24 = 0
    ddr4_cs1_dq25 = 0
    ddr4_cs1_dq26 = 0
    ddr4_cs1_dq27 = 0
    ddr4_cs1_dq28 = 0
    ddr4_cs1_dq29 = 0
    ddr4_cs1_dq30 = 0
    ddr4_cs1_dq31 = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "ddr4", "ddr2", "ddr3", encoding="I", bitmasks=[(0, 8), (16, 8), (24, 8)])
        self.map(0, 4, "lp2", "lp3", "lp4", encoding="I", bitmasks=[(8, 8), (16, 8), (24, 8)])
        for lp in [3, 2]:
            bitmasks = []
            attrs = []
            for i in range(8):
                bitmasks.append((4 * i, 4))
                attrs.append(f"lp{lp}_dq{i}")
            self.map(0, 4, *attrs, encoding="I", bitmasks=bitmasks)
        for cs in [0, 1]:
            bitmasks = []
            attrs = []
            for i in range(32):
                bitmasks.append((2 * i, 2))
                attrs.append(f"ddr4_cs{cs}_qd{i}")
            self.map(0, 8, *attrs, encoding="Q", bitmasks=bitmasks)
