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


class Iomux(block.MappedBlock, common.Printable):
    addr = 0

    def __init__(self, buffer, start=None):
        block.MappedBlock.__init__(self, buffer, start=start)
        self.map(0, 4, "addr", encoding="I")
