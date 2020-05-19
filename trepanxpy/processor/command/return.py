# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2013-2015, 2020 Rocky Bernstein
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
import os.path as osp, sys

from trepan.processor.command.base_cmd import DebuggerCommand


class ReturnCommand(DebuggerCommand):
    """**return** [*value*]

Cause an immediate return giving *value* as the return value.
If no value is specified, we'll use `None`.

See also:
---------

`step`, `stepi`.
"""

    aliases = ("ret",)
    category = "running"
    execution_set = ["Running"]
    min_args = 0
    max_args = 1
    name = osp.basename(__file__).split(".")[0]
    need_stack = True
    short_help = "Immediate return with value"

    def run(self, args):
        proc = self.proc
        if proc.stack is None:
            return False

        if len(args) == 0:
            proc.vm.return_value = None
        else:
            text = self.proc.current_command[len(self.proc.cmd_name):]
            pass
        text = text.strip()
        try:
            proc.vm.return_value = proc.eval(text)
        except:
            pass

        proc.return_status = "return"
        proc.continue_running = True  # Break out of command read loop
        return True

    pass


if __name__ == "__main__":
    from trepan.processor.command.mock import MockDebugger
    from xpython.vmtrace import PyVMTraced
    d = MockDebugger()
    proc = d.core.processor
    proc.vm = PyVMTraced(None)
    cmd = ReturnCommand(d.core.processor)

    def demo_return(cmd):
        for c in (
            ["return", "1"],
            ["return", "wrong", "number", "of", "args"],
            ["return", "5"],
        ):
            proc.vm.return_status = "Initial"
            proc.continue_running = False
            proc.stack = [(sys._getframe(0), 14,)]
            result = cmd.run(c)
            print("Execute result: %s" % result)
            print(
                "continue_running: %s, return status: %s"
                % (proc.continue_running,
                   proc.vm.return_status)
            )
            pass
        return

    demo_return(cmd)
    pass
