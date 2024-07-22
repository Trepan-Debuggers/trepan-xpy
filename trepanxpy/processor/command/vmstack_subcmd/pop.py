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


# Class has to start out with Vmstack not VMStack or anything else, in order
# for subcommand matching to work properly
class VmstackPop(DebuggerSubcommand):
    """**vmstack pop**

Pop a VM evaluation stack entry

Examples
--------

    vmstack pop

See Also
--------

`vmstack push`
"""

    in_list    = True
    min_abbrev = len('po')
    max_args = 1
    need_stack = True
    short_help = "Pop a value off the VM evaluation stack"

    def run(self, args):
        if self.core.is_running():
            proc = self.proc

            n = len(args)
            if n == 1:
                # FIXME add popping n entries
                count = 1
            else:
                count = 1

            result = proc.vm.frame.stack.pop()
            self.msg(f"VM stack popped {count} items: {result}, type {type(result)}")

        return None

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run

    demo_run(VmstackPop, [])
    pass
