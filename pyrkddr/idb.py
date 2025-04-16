"""
 Copyright (C) 2024 boogie

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

import ctypes
import hashlib
import operator

from pyrkddr import common


IDBHASH = [None, hashlib.sha256, hashlib.sha512]
IDBV2_MAGIC = b"RKNS"
HASHSIZE = 64
SIGNSIZE = 512


class c_idbentry_v2(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("offset", ctypes.c_uint16),
        ("blocks", ctypes.c_uint16),
        ("address", ctypes.c_uint32),
        ("flag", ctypes.c_uint32),
        ("counter", ctypes.c_uint32),
        ("reserved0", ctypes.c_byte * 8),
        ("hash", ctypes.c_byte * HASHSIZE),
        ]


class c_idbheader_v2(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic", ctypes.c_char * 4),
        ("reserved0", ctypes.c_byte * 4),
        ("offset", ctypes.c_uint16),
        ("numentries", ctypes.c_uint16),
        ("flags", ctypes.c_uint32),
        ("reserved1", ctypes.c_byte * 104),
        ("entries", c_idbentry_v2 * 4),
        ("reserved2", ctypes.c_byte * 1064),
        ("signature", ctypes.c_byte * SIGNSIZE),
        ]


def hashblock(buffer, hashtype, size, given=None):
    if not hashtype < len(IDBHASH):
        # signed?
        raise common.RkDdrException(f"Unknown hash type {hashtype}")
    hashfunc = IDBHASH[hashtype]
    if not hashfunc:
        raise common.RkDdrException(f"Unhashed idb")
        return given
    m = hashfunc()
    m.update(buffer)
    hashvalue = m.digest()
    # pad until end
    hashvalue += b"\x00" * (size - len(hashvalue))
    if given:
        if hashvalue != given:
            raise common.RkDdrException(f"IDB hash is {given} but expected {hashvalue}")
    return hashvalue


class IdEntry(common.Printable):
    def __init__(self, idb, entry):
        self._idb = idb
        self._entry = entry
        self.counter = self._entry.counter
        self.blocks = self._entry.blocks
        self.offset = self._entry.offset
        self.hash = bytes(self._entry.hash)
        self._blob = None

    @property
    def blob(self):
        return self._blob

    @blob.setter
    def blob(self, buffer):
        if not len(buffer) == len(self._blob):
            raise common.RkDdrException(f"Blob size is expected {len(self._blob)} but is {len(buffer)}")
        newhash = hashblock(buffer, self._idb.hashtype, 64)
        self._entry.hash = (ctypes.c_byte * HASHSIZE)(*newhash)
        self._blob = buffer
        newsign = hashblock(bytes(self._idb._idb)[:-SIGNSIZE], self._idb.hashtype, SIGNSIZE)
        self._idb.signature = newsign
        self._idb._idb.signature = (ctypes.c_byte * SIGNSIZE)(*newsign)


class IdBlock(common.Printable):
    @staticmethod
    def checkmagic(header):
        return header[0:4] == IDBV2_MAGIC

    def __init__(self, header):
        self.block = None
        self._idb = c_idbheader_v2.from_buffer_copy(header)
        self.hashtype = self._idb.flags & 0xf
        self.numentries = self._idb.numentries
        self.signature = hashblock(header[:-SIGNSIZE], self.hashtype, SIGNSIZE, bytes(self._idb.signature))
        self.entries = [IdEntry(self, x) for x in self._idb.entries if x.counter]
        self.entries.sort(key=operator.attrgetter("counter"))

    def read(self, f):
        self.block = int((f.tell() - ctypes.sizeof(c_idbheader_v2)) / common.BLOCK_SIZE)
        for entry in self.entries:
            f.seek((self.block + entry.offset) * common.BLOCK_SIZE)
            entry._blob = f.read(entry.blocks * common.BLOCK_SIZE)
            entry.hash = hashblock(entry._blob, self.hashtype, HASHSIZE, bytes(entry.hash))

    def dump(self):
        buffer = bytes(self._idb)
        cursor = self.block * common.BLOCK_SIZE + ctypes.sizeof(self._idb)
        for entry in self.entries:
            blobcursor = (self.block + entry.offset) * common.BLOCK_SIZE
            if blobcursor < cursor:
                raise common.RkDdrException(f"Overlapping idb blobs {blobcursor}, {cursor}")
            # pad if there are gaps
            buffer += b"\x00" * (blobcursor - cursor)
            buffer += entry.blob
            cursor = blobcursor + entry.blocks * common.BLOCK_SIZE
        return buffer


def iteridbs(f):
    while True:
        block = f.read(common.BLOCK_SIZE)
        if not block:
            break
        if IdBlock.checkmagic(block):
            block += f.read(common.BLOCK_SIZE * 3)
            try:
                idblock = IdBlock(block)
                idblock.read(f)
                yield idblock
            except common.RkDdrException:
                continue
