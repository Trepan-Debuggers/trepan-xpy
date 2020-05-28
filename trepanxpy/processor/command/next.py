# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2013, 2015, 2020 Rocky Bernstein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os.path as osp

from xpython.vmtrace import (
    PyVMEVENT_ALL,
    PyVMEVENT_INSTRUCTION,
    PyVMEVENT_STEP_OVER,
    )

from trepan.processor.command.base_cmd import DebuggerCommand

# Our local modules

class NextCommand(DebuggerCommand):
    """**next**[**+**|**-**] [*count*]

Execute the current simple statement stopping at the next event but
ignoring steps into function calls at this level,

With an integer argument, perform `next` that many times. However if
an exception occurs at this level, or we *return*, *yield* or the
thread changes, we stop regardless of count.

A suffix of `+` on the command or an alias to the command forces to
move to another line, while a suffix of `-` does the opposite and
disables the requiring a move to a new line. If no suffix is given,
the debugger setting 'different-line' determines this behavior.

See also:
---------

`step`, `skip`, `jump` (there's no `hop` yet), `continue`, and
`finish` for other ways to progress execution.
"""

    aliases = ("next+", "next-", "n", "n-", "n+")
    category = "running"
    execution_set = ["Running"]
    min_args = 0
    max_args = 1
    name = osp.basename(__file__).split(".")[0]
    need_stack = True
    short_help = "Step over"

    def run(self, args):
        proc = self.proc
        core = self.core
        if len(args) <= 1:
            core.step_ignore = 0
        else:
            pos = 1
            if pos == len(args) - 1:
                core.step_ignore = self.proc.get_int(args[pos], default=1,
                                                          cmdname='step')
                if self.core.step_ignore is None: return False
                # 0 means stop now or step 1, so we subtract 1.
                core.step_ignore -= 1
                pass
            elif pos != len(args):
                self.errmsg("Invalid additional parameters %s"
                            % ' '.join(args[pos]))
                return False
            pass

        # Add "step over" to all event flags, but remove instruction events.
        proc.vm.frame.event_flags = (PyVMEVENT_ALL | PyVMEVENT_STEP_OVER) ^ PyVMEVENT_INSTRUCTION

        core.different_line   = True # Mcmdfns.want_different_line(args[0], self.settings['different'])
        core.stop_level       = None
        core.last_frame       = None
        core.stop_on_finish   = False
        proc.continue_running = True  # Break out of command read loop
        return True
    pass

if __name__ == '__main__':
    from trepan.processor.command.mock import MockDebugger

    d = MockDebugger()
    cmd = NextCommand(d.core.processor)
    for c in (["n", "5"], ["next", "1+2"], ["n", "foo"]):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print("Run result: %s" % result)
        print(
            "step_ignore %d, continue_running: %s"
            % (d.core.step_ignore, cmd.continue_running,)
        )
        pass
    for c in (["n"], ["next+"], ["n-"]):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print(cmd.core.different_line)
        pass
    pass
