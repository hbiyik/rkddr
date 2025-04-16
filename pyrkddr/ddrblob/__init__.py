from pyrkddr import block
from pyrkddr import common
from . import header
from . import glob
from . import ddr
from . import dq
from . import skew
from . import hash


MAGIC = header.MAGIC


class V2(common.Printable):
    header = header.SdramInfov2
    glob = glob.Info
    lp2 = ddr.Ddr234Lp23
    ddr2 = ddr.Ddr234Lp23
    lp3 = ddr.Ddr234Lp23
    ddr3 = ddr.Ddr234Lp23
    lp4 = ddr.Lp4
    ddr4 = ddr.Ddr234Lp23
    lp5 = ddr.Lp4
    ddr5 = ddr.Ddr234Lp23
    skew = skew.Skew
    dq = dq.Map

    def __init__(self, buffer, start=None):
        if self.header == V2.header:
            self.header = V2.header(buffer, start)
        self.glob = self.header.getblock("glob", V2.glob)
        self.lp2 = self.header.getblock("lp2", V2.lp2)
        self.ddr2 = self.header.getblock("ddr2", V2.ddr2)
        self.lp3 = self.header.getblock("lp3", V2.lp3)
        self.ddr3 = self.header.getblock("ddr3", V2.ddr3)
        self.lp4 = self.header.getblock("lp4", V2.lp4)
        self.ddr4 = self.header.getblock("ddr4", V2.ddr4)
        self.lp5 = self.header.getblock("lp5", V2.lp5)
        self.ddr5 = self.header.getblock("ddr5", V2.ddr5)
        self.skew = self.header.getblock("skew", V2.skew)
        self.dq = self.header.getblock("dq", V2.dq)


class V3(V2):
    header = header.SdramInfov3
    lp4x = ddr.Lp4
    lp4hash = hash.Mask

    def __init__(self, buffer, start=None):
        if self.header == V3.header:
            self.header = self.header = V2.header(buffer, start)
        V2.__init__(self, buffer, start=start)
        self.lp4x = self.header.getblock("lp4x", V3.lp4x)
        self.lp4hash = self.header.getblock("lp4hash", V3.lp4hash)


class V4(V3):
    header = header.SdramInfov4
    lp5hash = hash.Mask
    ddr5hash = hash.Mask
    ddr4hash = hash.Mask
    lp3hash = hash.Mask
    ddr3hash = hash.Mask
    lp2hash = hash.Mask
    ddr2hash = hash.Mask

    def __init__(self, buffer, start=None):
        self.header = self.header = V4.header(buffer, start)
        V3.__init__(self, buffer, start=start)
        self.lp5hash = self.header.getblock("lp5hash", V4.lp5hash)
        self.ddr5hash = self.header.getblock("ddr5hash", V4.ddr5hash)
        self.ddr4hash = self.header.getblock("ddr4hash", V4.ddr4hash)
        self.lp3hash = self.header.getblock("lp3hash", V4.lp3hash)
        self.ddr3hash = self.header.getblock("ddr3hash", V4.ddr3hash)
        self.lp2hash = self.header.getblock("lp2hash", V4.lp2hash)
        self.ddr2hash = self.header.getblock("ddr2hash", V4.ddr2hash)


class V5(common.Printable):
    header = header.SdramInfov4
    glob = glob.Info
    lp2 = ddr.Ddr234Lp23_v5
    ddr2 = ddr.Ddr234Lp23_v5
    lp3 = ddr.Ddr234Lp23_v5
    ddr3 = ddr.Ddr234Lp23_v5
    lp4 = ddr.Lp4
    lp4x = ddr.Lp4
    ddr4 = ddr.Ddr234Lp23_v5
    lp5 = ddr.Lp4
    ddr5 = ddr.Ddr234Lp23_v5
    skew = skew.Skew
    dq = dq.Map
    lp5hash = hash.Mask
    ddr5hash = hash.Mask
    lp4hash = hash.Mask
    ddr4hash = hash.Mask
    lp3hash = hash.Mask
    ddr3hash = hash.Mask
    lp2hash = hash.Mask
    ddr2hash = hash.Mask

    def __init__(self, buffer, start=None):
        self.header = V5.header(buffer, start)
        self.glob = self.header.getblock("glob", V5.glob)
        self.lp2 = self.header.getblock("lp2", V5.lp2)
        self.ddr2 = self.header.getblock("ddr2", V5.ddr2)
        self.lp3 = self.header.getblock("lp3", V5.lp3)
        self.ddr3 = self.header.getblock("ddr3", V5.ddr3)
        self.lp4 = self.header.getblock("lp4", V5.lp4)
        self.lp4x = self.header.getblock("lp4x", V5.lp4x)
        self.ddr4 = self.header.getblock("ddr4", V5.ddr4)
        self.lp5 = self.header.getblock("lp5", V5.lp5)
        self.ddr5 = self.header.getblock("ddr5", V5.ddr5)
        self.skew = self.header.getblock("skew", V5.skew)
        self.dq = self.header.getblock("dq", V5.dq)
        self.lp5hash = self.header.getblock("lp5hash", V5.lp5hash)
        self.ddr5hash = self.header.getblock("ddr5hash", V5.ddr5hash)
        self.lp4hash = self.header.getblock("lp4hash", V5.lp4hash)
        self.ddr4hash = self.header.getblock("ddr4hash", V5.ddr4hash)
        self.lp3hash = self.header.getblock("lp3hash", V5.lp2hash)
        self.ddr3hash = self.header.getblock("ddr3hash", V5.ddr3hash)
        self.lp2hash = self.header.getblock("lp2hash", V5.lp2hash)
        self.ddr2hash = self.header.getblock("ddr2hash", V5.ddr2hash)


def get(version):
    versions = {2: V2, 3: V3, 4: V4, 5: V5}
    return versions.get(version)
