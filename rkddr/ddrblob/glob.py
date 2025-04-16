'''
Created on Apr 16, 2025

@author: boogie
'''
from rkddr import block


class Uart(block.MappedBlock, block.Printable):
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


class Idle(block.MappedBlock, block.Printable):
    sr = 0
    pr = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "pr", "sr", encoding="I", bitmasks=[(0, 16),
                                                           (16, 16),
                                                           ])


class Channel(block.MappedBlock, block.Printable):
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


class T2(block.MappedBlock, block.Printable):
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
                       "res_space_remap_all",  "auto_precharge_en", "derate_en", "per_bank_ref_en", "link_ecc_en", "ext_temp_ref",
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


class Info(block.MappedBlock, block.Printable):
    uart = Uart
    idle = Idle
    channel = Channel
    t2 = T2
    _reserved0 = 0
    _reserved1 = 0
    _reserved2 = 0
    _reserved3 = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start)
        self.addblock(uart=Uart, idle=Idle, channel=Channel, tr=T2)
        self.map(0, 4 * 4, "_reserved0", "_reserved1", "_reserved2", "_reserved3",
                 encoding="I" * 4)
