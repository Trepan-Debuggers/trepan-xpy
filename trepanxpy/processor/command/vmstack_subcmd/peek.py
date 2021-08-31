# -*- coding: utf-8 -*-
#   Copyright (C) 2021 Rocky Bernstein
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

from trepan.processor.command.base_subcmd import DebuggerSubcommand
from trepan.processor.cmdfns import get_an_int


# Class has to start out with Vmstack not VMStack or anything else, in order
# for subcommand matching to work properly
class VmstackPeek(DebuggerSubcommand):
    """**vmstack peek** *i*

Look at VM evaluation stack entry *i*

Examples
--------

    vmstack peek 1

See Also
--------

`vmstack pop`, `vmstack push`
"""

    in_list    = True
    min_abbrev = len('pe')
    min_args = 0
    max_args = 1
    need_stack = True
    short_help = "look at a VM evaluation stack entry"

    def run(self, args):
        if self.core.is_running():
            proc = self.proc

            n = len(proc.vm.frame.stack)
            if n == 0:
                self.errmsg("VM evaluation stack is empty - nothing to peek at at")
                return

            if len(args) == 0:
                number = 0
            else:
                print(args)
                number = get_an_int(
                    self.errmsg,
                    args[0],
                    "The 'peek' command requires an integer greater than 0.",
                    0, n-1
                )
                if number is None:
                    return
            # FIXME: vm.peek seems to be 1 origin. It should have been 0 origin I think.
            result = proc.vm.peek(number+1)
            self.msg(f"VM evaluation stack at {number}: {result} {type(result)}")
        return None

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run

    demo_run(VmstackPeek, [])
    pass
