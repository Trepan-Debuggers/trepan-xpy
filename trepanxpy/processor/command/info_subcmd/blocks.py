# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSubcommand


class InfoBlocks(DebuggerSubcommand):
    """**info blocks**

Show the block-unwinding structure of the current frame

See also:
---------

`show stack`,
"""

    min_abbrev = 1  # Need at least info 'b'
    max_args = 0
    need_stack = True
    short_help = "Show the block-unwinding structure of the current frame"

    def run(self, args):
        """Block Stack."""
        frame = self.proc.vm.frame
        if not hasattr(frame, "block_stack"):
            self.errmsg("frame %s doesn't have a block stack" % frame)
        else:
            block_stack = frame.block_stack
            if len(block_stack) == 0:
                self.msg("Block stack is empty")
            else:
                for i, obj in enumerate(reversed(block_stack)):
                    self.msg("%2d: %s" % (i, obj))
        return False

    pass


# if __name__ == "__main__":
#     from trepan.processor.command import mock, info as Minfo

#     d, cp = mock.dbg_setup()
#     i = Minfo.InfoCommand(cp)
#     sub = InfoBlocks(i)
#     sub.run([])
