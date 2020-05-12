# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein
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

import logging

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSetBoolSubcommand


class SetLogTrace(DebuggerSetBoolSubcommand):
    """**set logtrace** [ **on** | **off** ]

Show logtrace PyVM "debug" and "info" messages.
"""

    in_list    = True
    min_abbrev = len('lo')


    def run(self, args):
        super().run(args)
        if self.debugger.settings["logtrace"]:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)
        return

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run
    demo_run(SetLogTrace)
    pass
