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
import struct
import functools

from pyrkddr import common


class MappedList(list):
    def __init__(self, f, start, encoding):
        self._start = start
        self._f = f
        if encoding.startswith(">") or encoding.startswith("<"):
            self._endian = encoding[0]
            self._encoding = encoding[1:]
        else:
            self._encoding = encoding
            self._endian = "<"

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __getitem__(self, i):
        encoding = self._encoding[i]
        offset = struct.calcsize(self._encoding[:i])
        size = struct.calcsize(self._encoding[i])
        self._f.seek(self._start + offset)
        return struct.unpack(self._endian + encoding, self._f.read(size))[0]

    def __setitem__(self, index, item):
        encoding = self._encoding[index]
        offset = struct.calcsize(self._encoding[:index])
        self._f.seek(self._start + offset)
        self._f.write(struct.pack(self._endian + encoding, item))

    def __len__(self):
        return len(self._encoding)

    def __repr__(self):
        return repr(list(self))


class MappedBlock:
    def __init__(self, block, start=None):
        self._map = []
        self._attrs = {}
        self._f = block
        self._start = start or self._f.tell()
        self._size = 0

    def dumphandler(self):
        self._f.seek(0)
        return self._f.read()

    def _arrsize(self, name):
        arrsize = 1
        if "*" in name:
            name, arrsize = name.split("*")
            arrsize = int(arrsize)
        return name, arrsize

    def addblock(self, **kwargs):
        for attrname, attrtype in kwargs.items():
            attr = attrtype(self._f, self.start + self.size)
            self._size += attr.size
            setattr(self, attrname, attr)

    def getrange(self, attr):
        for _offset, _size, names, encoding, bitmasks in self._map:
            if attr not in names:
                continue
            index = names.index(attr)
            minrange = 0
            if not bitmasks:
                for replace in ["@", ">", "<", "=", "!"]:
                    encoding = encoding.replace(replace, "")
                encoding = encoding[index]
                size = struct.calcsize(encoding)
                maxrange = 2 ** (size * 8) - 1
                if encoding.islower():
                    maxrange = int((maxrange - 1) / 2)
                    minrange = -maxrange - 1
            else:
                _offset, size = bitmasks[index]
                maxrange = 2 ** size - 1
            return minrange, maxrange

    @property
    def size(self):
        return self._size

    @property
    def start(self):
        return self._start

    def map(self, offset, size, *names, le=True, encoding=None, bitmasks=None):
        for name in names:
            if name in self._attrs:
                raise AttributeError(f"{name} is already mapped")
        encoding = "<" + encoding if le else ">" + encoding
        self._map.append([offset + self.start + self.size, size, [self._arrsize(x)[0] for x in names], encoding, bitmasks])
        self._size += struct.calcsize(encoding)
        for name in names:
            name, arrsize = self._arrsize(name)
            setattr(self.__class__, name, property(functools.partial(self.__class__._getmap, attr=name),
                                                   functools.partial(self.__class__._setmap, attr=name)))
            self._attrs[name] = arrsize

    def _decodemap(self, attr, names, encoding, bitmasks, data_or_offset):
        attrs = struct.unpack(encoding, data_or_offset)
        index = names.index(attr)
        if not bitmasks:
            return attrs[index]
        else:
            offset, size = bitmasks[index]
            return common.shiftmask(attrs[0], offset, size)

    def _getmap(self, attr):
        for offset, size, names, encoding, bitmasks in self._map:
            if attr in names:
                if self._attrs[attr] == 1:
                    self._f.seek(offset)
                    data = self._f.read(size)
                    return self._decodemap(attr, names, encoding, bitmasks, data)
                else:
                    # array
                    return MappedList(self._f, offset, encoding)
        raise AttributeError(f"{attr} is not available")

    def _setmap(self, value, attr):
        for offset, size, names, encoding, bitmasks in self._map:
            if attr in names:
                if self._attrs[attr] == 1:
                    values = []
                    self._f.seek(offset)
                    data = self._f.read(size)
                    for name in names:
                        if name == attr:
                            values.append(value)
                        else:
                            values.append(self._decodemap(name, names, encoding, bitmasks, data))
                    if not bitmasks:
                        newdata = struct.pack(encoding, *values)
                    else:
                        newvalue = 0
                        for i, (bitoffset, size) in enumerate(bitmasks):
                            newvalue |= common.maskshift(values[i], size, bitoffset)
                        newdata = struct.pack(encoding, newvalue)
                    self._f.seek(offset)
                    self._f.write(newdata)
                else:
                    # array
                    mlist = self._getmap(attr)
                    for i, v in enumerate(values):
                        mlist[i] = v
                return
        raise AttributeError(f"{attr} is not available")
