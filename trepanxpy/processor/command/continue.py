# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2013, 2015, 2017, 2020 Rocky Bernstein
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

from trepan.processor.command.base_cmd import DebuggerCommand
from trepan.processor.cmdbreak import parse_break_cmd, set_break

from xpython.vmtrace import (
    PyVMEVENT_ALL,
    PyVMEVENT_CALL,
    PyVMEVENT_FATAL,
    PyVMEVENT_INSTRUCTION,
    PyVMEVENT_LINE,
)


class ContinueCommand(DebuggerCommand):
    """**continue**

Leave the debugger read-eval print loop and continue
execution. Subsequent entry to the debugger however may occur via
breakpoints or explicit calls, or exceptions.

Examples:
---------

    continue          # Continue execution
    continue 5        # Continue with a one-time breakpoint at line 5
    continue basename # Go to os.path.basename if we have basename imported
    continue /usr/lib/python3.8/posixpath.py:110 # Possibly the same as
                                                 # the above using file
                                                 # and line number

See also:
---------

`step` `jump`, `next`, `finish` and `help syntax location`
"""

    aliases = ("c", "continue!")
    execution_set = ["Running"]
    short_help = "Continue execution of debugged program"

    DebuggerCommand.setup(locals(), category="running", max_args=1, need_stack=True)

    def run(self, args):
        proc = self.proc
        if len(args) > 1:
            # FIXME: DRY this code. Better is to hook into tbreak.
            func, filename, lineno, condition = parse_break_cmd(proc, args)

            if not set_break(
                self, func, filename, lineno, condition, True, args
            ):
                return False
        elif args[0][-1] == "!":
            proc.vm.frame.event_flags = proc.vm.event_flags = 0  # ignore all events
        else:
            # Until we hook in breakpoints into the debugger proper, we'll
            # treat continue like step in the VM interpreter but not
            # from our filtering process
            proc.vm.frame.event_flags = PyVMEVENT_ALL
            proc.core.event_flags = (
                PyVMEVENT_LINE | PyVMEVENT_INSTRUCTION |
                PyVMEVENT_CALL | PyVMEVENT_FATAL
            )

        self.core.step_ignore = -1
        self.proc.continue_running = True  # Break out of command read loop
        self.return_status = "continue"  # Tell interpreter to continue running

    pass


if __name__ == "__main__":
    import sys
    from trepan import debugger as Mdebugger

    d = Mdebugger.Trepan()
    cmd = ContinueCommand(d.core.processor)
    cmd.proc.frame = sys._getframe()
    cmd.proc.setup()

    for c in (
        ["continue", "wrong", "number", "of", "args"],
        ["c", "5"],
        ["continue", "1+2"],
        ["c", "foo"],
    ):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print("Run result: %s" % result)
        print(
            "step_ignore %d, continue_running: %s"
            % (d.core.step_ignore, cmd.continue_running,)
        )
        pass
    pass
