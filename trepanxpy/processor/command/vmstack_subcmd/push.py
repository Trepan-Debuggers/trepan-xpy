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
class VmstackPush(DebuggerSubcommand):
    """**vmstack push** *value*

Push a value onto the VM evaluation

Examples
--------

    vmstack push "foo"

See Also
--------

`vmstack pop`
"""

    in_list    = True
    min_abbrev = len('pu')
    min_args = 1
    max_args = 1
    need_stack = True
    short_help = "Pop a value off the VM evaluation stack"

    def run(self, args):
        if self.core.is_running():
            proc = self.proc

            text = args[0]
            proc.vm.push(eval(text))
            self.msg(f"VM pushed: {text}")

        return None

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run

    demo_run(VmstackPush, ["abc"])
    pass
