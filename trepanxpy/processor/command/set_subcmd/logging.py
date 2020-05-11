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

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSetBoolSubcommand


class SetLogging(DebuggerSetBoolSubcommand):
    """**set logging** [ **on** | **off** ]

Show logging PyVM "debug" and "info" messages.
"""

    in_list    = True
    min_abbrev = len('lo')


    def run(self, args):
        from trepan.api import debug; debug()
        super().__init__(args)
        return

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(SetLogging)
    pass
