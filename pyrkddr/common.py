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
BLOCK_SIZE = 512
IDBOFFSET = 64 * BLOCK_SIZE
MAXBACKUPS = 10


class RkDdrException(Exception):
    pass


class Printable:
    def iterattrs(self):
        for k, _v in self.__dict__.items():
            if not k.startswith("_"):
                yield k, getattr(self, k)

        if hasattr(self, "_attrs"):
            for k, _arrlen in self._attrs.items():
                if k.startswith("_"):
                    continue
                yield k, getattr(self, k)

    def __repr__(self):
        txt = f"[{self.__class__.__name__}]\n"
        for k, v in self.iterattrs():
            val = ""
            for line in repr(v).split("\n"):
                if not line:
                    continue
                val += f" {line}\n"
            txt += f"{k} ={val}"
        return txt


def maskshift(val, mask, shift):
    return (val & (2 ** mask - 1)) << shift


def shiftmask(val, shift, mask):
    return (val >> shift) & (2 ** mask - 1)
