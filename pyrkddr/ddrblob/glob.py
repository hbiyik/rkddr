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


class Uart(block.MappedBlock, common.Printable):
    # definition of class variables here are only for IDE auto complete
    # not needed for actual runtime
    id = 0
    iomux = 0
    baudrate = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "baudrate", "iomux", "id", encoding="I", bitmasks=[(0, 24),
                                                                          (24, 4),
                                                                          (28, 4),
                                                                          ])


class Idle(block.MappedBlock, common.Printable):
    sr = 0
    pr = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "pr", "sr", encoding="I", bitmasks=[(0, 16),
                                                           (16, 16),
                                                           ])


class Channel(block.MappedBlock, common.Printable):
    first_scan = 0
    mask = 0
    stride_ype = 0
    standby_idle = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "standby_idle", "stride_ype", "mask", "first_scan",
                 encoding="I", bitmasks=[(0, 8),
                                         (8, 8),
                                         (16, 8),
                                         (24, 8),
                                         ])


class T2(block.MappedBlock, common.Printable):
    ext_temp_ref = 0
    link_ecc_en = 0
    per_bank_ref_en = 0
    derate_en = 0
    auto_precharge_en = 0
    res_space_remap_all = 0
    res_space_premap_portion = 0
    rd_vref_scan_en = 0
    wr_vref_scan_en = 0
    eye_2d_scan_en = 0
    dis_train_print = 0
    ssmod_downspread = 0
    ssmod_div = 0
    ssmod_spread = 0
    ddr_2t = 0
    _reservedbit0 = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, 'ddr_2t', 'ssmod_spread', 'ssmod_div', 'ssmod_downspread',
                       'dis_train_print', "res_space_premap_portion", 'rd_vref_scan_en', 'wr_vref_scan_en', 'eye_2d_scan_en',
                       "res_space_remap_all", "auto_precharge_en", "derate_en", "per_bank_ref_en", "link_ecc_en", "ext_temp_ref",
                       '_reservedbit0',
                       encoding="I", bitmasks=[(0, 1),
                                               (1, 8),
                                               (9, 8),
                                               (17, 2),
                                               (19, 1),
                                               (20, 1),
                                               (21, 1),
                                               (22, 1),
                                               (23, 1),
                                               (24, 1),
                                               (25, 1),
                                               (26, 1),
                                               (27, 1),
                                               (28, 1),
                                               (29, 2),
                                               (31, 1),
                                               ])


class Config(block.MappedBlock, common.Printable):
    tpl_log_en = 0
    spl_log_en = 0
    optee_log_en = 0
    atf_log_en = 0
    uboot_log_en = 0
    pstore_buf_size = 0
    pstore_base_addr = 0
    boost_fsp = 0
    page_close = 0
    dfs_disable = 0
    first_init_dram_type = 0
    trfc_mode = 0
    periodic_interval = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 8, "tpl_log_en", "spl_log_en", "optee_log_en", "atf_log_en", "uboot_log_en", "reserved0", "pstore_buf_size", "pstore_base_addr", "reserved1"
                 "boost_fsp", "page_close", "dfs_disable", "first_init_dram_type", "trfc_mode", "periodic_interva", "reserved2",
                  encoding="Q", bitmasks=[(0, 1),
                                          (1, 1),
                                          (2, 1),
                                          (3, 1),
                                          (4, 1),
                                          (5, 7),
                                          (12, 4),
                                          (16, 8),
                                          (24, 8),
                                          (32 + 0, 3),
                                          (32 + 3, 1),
                                          (32 + 4, 1),
                                          (32 + 5, 4),
                                          (32 + 9, 2),
                                          (32 + 11, 7),
                                          (32 + 18, 14),
                                          ])


class Info(block.MappedBlock, common.Printable):
    uart = Uart
    idle = Idle
    channel = Channel
    t2 = T2
    config = Config
    _reserved2 = 0
    _reserved3 = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start)
        self.addblock(uart=Uart, idle=Idle, channel=Channel, tr=T2, cofig=Config)
        self.map(0, 4 * 2, "_reserved2", "_reserved3",
                 encoding="I" * 4)
