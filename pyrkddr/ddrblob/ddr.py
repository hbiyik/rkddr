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


class Ddr234Lp23(block.MappedBlock, common.Printable):
    freq = 0
    freq1 = 0
    freq2 = 0
    freq3 = 0
    freq4 = 0
    freq5 = 0
    dq_drv_when_odten_ohm = 0
    ca_drv_when_odten_ohm = 0
    clk_drv_when_odten_ohm = 0
    dq_drv_when_odten_ohm = 0
    dq_drv_when_odtoff_ohm = 0
    ca_drv_when_odtoff_ohm = 0
    clk_drv_when_odtoff_ohm = 0
    dq_drv_when_odtoff_ohm = 0
    odt_ohm = 0
    phy_odt_ohm = 0
    odt_pull_up_en = 0
    odt_pull_dn_en = 0
    phy_odt_en_freq = 0
    odt_en_freq = 0
    dq_sr_when_odten = 0
    ca_sr_when_odten = 0
    clk_sr_when_odten = 0
    dq_sr_when_odtoff = 0
    ca_sr_when_odtoff = 0
    clk_sr_when_odtoff = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "freq", "freq1", encoding="I", bitmasks=[(0, 12), (12, 12)])
        self.map(0, 4, "freq2", "freq3", encoding="I", bitmasks=[(0, 12), (12, 12)])
        self.map(0, 4, "freq4", "freq5", encoding="I", bitmasks=[(0, 12), (12, 12)])
        self.map(0, 4, "dq_drv_when_odten_ohm", "ca_drv_when_odten_ohm", "clk_drv_when_odten_ohm", "dq_drv_when_odten_ohm",
                 encoding="I", bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "dq_drv_when_odtoff_ohm", "ca_drv_when_odtoff_ohm", "clk_drv_when_odtoff_ohm", "dq_drv_when_odtoff_ohm",
                 encoding="I", bitmasks=[(0, 8), (8, 8), (16, 8), (24, 8)])
        self.map(0, 4, "odt_ohm", "phy_odt_ohm", "odt_pull_up_en", "odt_pull_dn_en",
                 encoding="I", bitmasks=[(0, 8), (8, 10), (18, 1), (19, 1)])
        self.map(0, 4, "phy_odt_en_freq", "odt_en_freq",
                 encoding="I", bitmasks=[(0, 12), (12, 12)])
        self.map(0, 4, "dq_sr_when_odten", "ca_sr_when_odten", "clk_sr_when_odten",
                 encoding="I", bitmasks=[(0, 8), (8, 8), (16, 8)])
        self.map(0, 4, "dq_sr_when_odtoff", "ca_sr_when_odtoff", "clk_sr_when_odtoff",
                 encoding="I", bitmasks=[(0, 8), (8, 8), (16, 8)])


class Ddr234Lp23_v5(Ddr234Lp23):
    phy_dq_vref_when_odten = 0
    dq_vref_when_odten = 0
    ca_vref_when_odten = 0
    phy_dq_vref_when_odtoff = 0
    dq_vref_when_odtoff = 0
    ca_vref_when_odtoff = 0

    def __init__(self, buffer, start=None):
        Ddr234Lp23.__init__(self, buffer, start=start)
        self.map(0, 4, "phy_dq_vref_when_odten", "dq_vref_when_odten", "ca_vref_when_odten",
                 encoding="I", bitmasks=[(0, 10), (10, 10), (20, 10)])
        self.map(0, 4, "phy_dq_vref_when_odtoff", "dq_vref_when_odtoff", "ca_vref_when_odtoff",
                 encoding="I", bitmasks=[(0, 10), (10, 10), (20, 10)])


class Lp4(Ddr234Lp23):
    ca_odten_freq_mhz = 0
    cs_drv_odten = 0
    cs_drv_odtoff = 0
    odte_ck = 0
    odte_cs_en = 0
    odtd_ca_en = 0
    phy_dq_vref_when_odten = 0
    dq_vref_when_odten = 0
    ca_vref_when_odten = 0
    phy_dq_vref_when_odtoff = 0
    dq_vref_when_odtoff = 0
    ca_vref_when_odtoff = 0

    def __init__(self, buffer, start=None):
        Ddr234Lp23.__init__(self, buffer, start=start)
        self.map(0, 4, "ca_odten_freq_mhz",
                 encoding="I", bitmasks=[(0, 12)])
        self.map(0, 4, "cs_drv_odten", "cs_drv_odtoff", "odte_ck", "odte_cs_en", "odtd_ca_en",
                 encoding="I", bitmasks=[(0, 8), (8, 8), (16, 1), (17, 1), (18, 1)])
        self.map(0, 4, "phy_dq_vref_when_odten", "dq_vref_when_odten", "ca_vref_when_odten",
                 encoding="I", bitmasks=[(0, 10), (10, 10), (20, 10)])
        self.map(0, 4, "phy_dq_vref_when_odtoff", "dq_vref_when_odtoff", "ca_vref_when_odtoff",
                 encoding="I", bitmasks=[(0, 10), (10, 10), (20, 10)])
