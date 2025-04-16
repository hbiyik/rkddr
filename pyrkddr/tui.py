'''
Created on Apr 18, 2025

@author: boogie
'''

import curses
import curses.textpad

from pyrkddr import block


class Screen:
    UP = -1
    DOWN = 1

    def __init__(self, blob, header=""):
        self.window = None
        self.headers = [header, ""]
        self.msg = ""

        self.width = 0
        self.height = 0
        curses.set_escdelay(25)
        self.init_curses()

        self.blob = blob
        self.block = None
        self.max_lines = curses.LINES - len(self.headers)
        self.prevs = []
        self.top = 0
        self.bottom = 0
        self.current = 0
        self.page = 0
        self.init(self.blob, None)

    def init(self, block, attrname, current=0):
        if self.block:
            self.prevs.append((self.block, attrname, self.current))
        self.block = block
        self.blockname = attrname
        self.top = 0
        self.bottom = len(list(self.iterblock()))
        self.current = current
        self.page = self.bottom // self.max_lines

    def back(self):
        self.block = None
        self.init(*self.prevs.pop())

    def init_curses(self):
        self.window = curses.initscr()
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)

        self.window.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)

        self.current = curses.color_pair(2)

        self.height, self.width = self.window.getmaxyx()

    def run(self):
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT or ch == curses.KEY_PPAGE:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT or ch == curses.KEY_NPAGE:
                self.paging(self.DOWN)
            elif ch == curses.ascii.LF or ch == curses.KEY_ENTER:
                self.select()
            elif ch == curses.KEY_BACKSPACE:
                if self.prevs:
                    self.back()
            elif ch == curses.ascii.ESC:
                if not self.prevs:
                    break
                self.back()

    def scroll(self, direction):
        next_line = self.current + direction
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return

    def paging(self, direction):
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return

        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def iterblock(self):
        idx = 0
        for attrname, attr in self.block.iterattrs():
            if attrname == "header":
                continue
            if attr is None:
                continue
            yield idx, attrname, attr
            idx += 1

    def setheader1(self, attr, attrname):
        vals = [">".join([x[1] for x in self.prevs if x is not None])]
        if isinstance(attr, block.MappedBlock):
            vals.append(attrname)
        else:
            minrange, maxrange = self.block.getrange(attrname)
            vals.append(f"{attrname}=[{minrange}-{maxrange}]")
        vals.append(self.msg)
        self.msg = ""
        self.headers[1] = " ".join(vals).strip()

    def display(self):
        self.height, self.width = self.window.getmaxyx()
        self.window.erase()
        row = 0
        for idx, attrname, attr in self.iterblock():
            if idx < self.top or idx >= self.top + self.max_lines:
                continue
            if isinstance(attr, block.MappedBlock):
                val = f"[{attrname}]"
            else:
                val = f"{attrname} = {attr}"
            if row == self.current:
                self.setheader1(attr, attrname)
                self.window.addstr(row + len(self.headers), 0, val, curses.color_pair(2))
            else:
                self.window.addstr(row + len(self.headers), 0, val, curses.color_pair(1))
            row += 1
        for row, header in enumerate(self.headers):
            self.window.addstr(row, 0, header + " " * (self.width - len(header)), curses.color_pair(4))
        self.window.refresh()

    def setattr(self, idx, attrname):
        minrange, maxrange = self.block.getrange(attrname)
        curses.echo()
        value = self.window.getstr(idx, len(attrname) + 3)
        curses.noecho()
        try:
            value = int(value)
        except Exception:
            self.msg = f"ERROR: Non integer Value {value}"
            return
        if value < minrange or value > maxrange:
            self.msg = f"ERROR: Value {value} is not in range {minrange}-{maxrange}"
            return
        self.msg = f"SUCCESS: {attrname} is set to {value}"
        setattr(self.block, attrname, value)

    def select(self):
        for idx, attrname, attr in self.iterblock():
            idx -= self.top
            if idx == self.current:
                if isinstance(attr, block.MappedBlock):
                    self.init(attr, attrname)
                else:
                    self.setattr(idx + len(self.headers), attrname)
