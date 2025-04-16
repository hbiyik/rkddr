import sys
from rkddr.ddrblob import header
from rkddr.ddrblob import glob

bin_path = sys.argv[1]


IndexMap = {
    "glob": glob.Info
    }

with open(bin_path, "rb") as f:
    while True:
        if f.read(4) == header.MAGIC:
            break
    hdr = header.SdramInfov2(f, f.tell() - 4)
    print(hdr)
    for indexname, index in hdr.iterattrs():
        if not isinstance(index, header.Index):
            continue
        dataType = IndexMap.get(indexname)
        if not dataType:
            continue
        data = dataType(f, hdr.start + index.offset * 4)
        print(data)
