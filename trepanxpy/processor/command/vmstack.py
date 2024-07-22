# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Rocky Bernstein
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

from trepan.processor.command.show import ShowCommand as Trepan3kShowCommand

class VMStackCommand(Trepan3kShowCommand):
    """**vmstack** *subcommand*

Generic command for working with the VM evaluation stack.  You can
give unique prefix of the name of a subcommand to get information
about just that subcommand.

Type `vmstack` for a list of *vmstack* subcommands and what they do.
Type `help vmstack *` for just a list of *vmstack* subcommands.
"""

    category = "vmstack"
    min_args = 0
    max_args = None
    name = osp.basename(__file__).split(".")[0]
    need_stack = False
    short_help = "Work with the VM evaluation stack"

    def __init__(self, proc, name="vmstack"):
        """Initialize vmstack subcommands. Note: instance variable name
        has to be setcmds ('vmstack' + 'cmds') for subcommand completion
        to work."""

        super().__init__(proc, name, "trepanxpy")
        new_cmdlist = []
        for subname in self.cmds.cmdlist:
            new_cmdlist.append(subname)
        self.cmds.cmdlist = new_cmdlist
        self._load_debugger_subcommands(name, "trepanxpy")


if __name__ == "__main__":
    from trepan.processor.command import mock

    d, cp = mock.dbg_setup()
    command = VMStackCommand(cp, "vmstack")
    command.run(["show"])
    pass
