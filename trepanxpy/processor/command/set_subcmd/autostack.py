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

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSetBoolSubcommand
from trepan.processor.cmdfns import run_set_bool, run_show_bool


class SetAutoStack(DebuggerSetBoolSubcommand):
    """**set autostack** [ **on** | **off** ]

Run the `info stack` command every time we enter the debugger.

See also:
---------

`show autostackc`
"""

    in_list = True
    min_abbrev = len("autos")

    info_stack_cmd = None

    def run(self, args):
        run_set_bool(self, args)
        if self.settings["autostack"]:
            if self.info_stack_cmd is None:
                info_cmd = self.proc.commands["info"]
                self.info_stack_cmd = info_cmd.cmds.lookup("stack").run
                pass
            self.proc.add_preloop_hook(self.run_infostack, 0)

        else:
            self.proc.remove_preloop_hook(self.run_infostack)
            pass
        run_show_bool(self, "Run `info stack` on debugger entry")
        return

    def run_infostack(self, args):
        if self.proc.frame:
            self.info_stack_cmd(["info", "stack"])
        return

    pass


if __name__ == "__main__":
    from trepan.processor.command.show_subcmd.__demo_helper__ import demo_run

    demo_run(SetAutoStack)
    pass
