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

import reprlib as Mrepr

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSubcommand


class InfoStack(DebuggerSubcommand):
    """**info stack**

Show the current frame's evaluation stack

See also:
---------

`info pc`, `info program`
"""

    min_abbrev = 2  # Need at least info 'pc'
    max_args = 0
    need_stack = True
    short_help = "Show Program Counter or Instruction Offset information"

    def run(self, args):
        """Evaluation Stack."""
        frame = self.proc.vm.frame
        if not hasattr(frame, "stack"):
            self.errmsg("frame %s doesn't have an evaluation stack" % frame)
        else:
            eval_stack = frame.stack
            if len(eval_stack) == 0:
                self.msg("Evaluation stack is empty")
            else:
                for i, obj in enumerate(reversed(eval_stack)):
                    self.msg("%2d: %s %s" % (i, type(obj), Mrepr.repr(obj)))
        return False

    pass


# if __name__ == "__main__":
#     from trepan.processor.command import mock, info as Minfo

#     d, cp = mock.dbg_setup()
#     i = Minfo.InfoCommand(cp)
#     sub = InfoStack(i)
#     sub.run([])
