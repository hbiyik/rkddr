import os
import io
import argparse

from rkddr import ddrblob
from rkddr import common
from rkddr import idb
from rkddr import tui


def openfile(fullpath):
    try:
        return open(fullpath, "rb+")
    except PermissionError:
        print(f"Dont have read+write access to {fullpath}")
    except FileNotFoundError:
        print(f"{fullpath} does not exist")
    except Exception as e:
        print(f"Error {e} happened while openning {fullpath}")


def findblob(buffer):
    f = io.BytesIO(buffer)
    while True:
        if f.read(4) == ddrblob.MAGIC:
            version = int.from_bytes(f.read(4), "little")
            Blob = ddrblob.get(version)
            if not Blob:
                return
            blob = Blob(f, f.tell() - 8)
            return blob


def findidb(f, offset=common.IDBOFFSET):
    f.seek(offset)
    block = f.read(common.BLOCK_SIZE)
    if not idb.IdBlock.checkmagic(block):
        return
    block += f.read(common.BLOCK_SIZE * 3)
    idblock = idb.IdBlock(block)
    idblock.read(f)
    if not idblock.entries:
        return
    return idblock


def showtui(blob, header=""):
    header = f"RKDDR: {header} with ddr blob version {blob.header.version}"
    screen = tui.Screen(blob, header)
    screen.run()


def blobfromidb(handler, offset=common.IDBOFFSET):
    idblock = findidb(handler, offset)
    if not idblock:
        return
    blob = findblob(idblock.entries[0].blob)
    if not blob:
        return
    return idblock, blob


def finddevice(fullpath):
    handler = openfile(fullpath)
    if not handler:
        return
    ret = blobfromidb(handler)
    if not ret:
        return
    idblock, blob = ret
    return handler, idblock, blob


def iterdevices():
    devtypes = ["mtd", "mmcblk", "sda", "sdb", "sdc", "sdd"]
    for devtype in devtypes:
        for path in os.listdir("/dev"):
            if path.startswith(devtype) and path.replace(devtype, "").isdigit():
                fullpath = os.path.join("/dev", path)
                ret = finddevice(fullpath)
                if not ret:
                    continue
                yield ret


def updatebuffer(handler, oldbuf, newbuf, offset):
    if not newbuf == oldbuf:
        isyes = input("Are you sure you want to save the changes [y/N]:")
        if not isyes.lower() == "y":
            print("Changes discarded")
            return
        handler.seek(offset)
        # some block devices requires zeroing first
        zero = b"\x00" * len(newbuf)
        handler.write(zero)
        handler.seek(offset)
        handler.write(newbuf)
        print("Changes saved")


def updateidb(handler, idblock, blob):
    oldidbbuf = idblock.dump()
    idblock.entries[0].blob = blob.header.dumphandler()
    newidbbuf = idblock.dump()
    updatebuffer(handler, oldidbbuf, newidbbuf, idblock.block * common.BLOCK_SIZE)


def main():
    parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
    parser.add_argument('-d', "--device", help='Work on on the DDR blob inside the found IDB of the given block device')
    parser.add_argument('-i', "--idb", help='Work on on the DDR blob inside the given IDB file')
    parser.add_argument('-b', "--blob", help='Work on on the DDR blob file given')
    args = parser.parse_args()

    handler = None
    if args.device:
        ret = finddevice(args.device)
        if not ret:
            return
        handler, idblock, blob = ret
        showtui(blob, f"TPL from '{handler.name}' at block {idblock.block}")
        updateidb(handler, idblock, blob)
    elif args.idb:
        handler = openfile(args.idb)
        if not handler:
            return
        ret = blobfromidb(handler, 0)
        if not ret:
            return
        idblock, blob = ret
        showtui(blob, f"IDB from '{handler.name}' at block 0")
        updateidb(handler, idblock, blob)
    elif args.blob:
        handler = openfile(args.blob)
        if not handler:
            return
        oldbuf = handler.read()
        blob = findblob(oldbuf)
        if not blob:
            return
        showtui(blob, f"BLOB from '{args.blob}'")
        updatebuffer(handler, oldbuf, blob.header.dumphandler(), 0)
    else:
        for handler, idblock, blob in iterdevices():
            showtui(blob, f"TPL from '{handler.name}' at block {idblock.block}")
            updateidb(handler, idblock, blob)
            break

    if handler:
        handler.close()


if __name__ == "__main__":
    main()
