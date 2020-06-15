# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.

# Helper function for Processor. Put here so we
# can use this in a couple of processors.

from typing import Any, Optional, Callable

from trepanxpy.fmt import format_instruction_with_highlight

class XPyPrintProcessor(object):
    """
    A processor that just prints out events as we see them. This
    is suitable for example for line/call tracing. We assume that the
    caller is going to filter out which events it wants printed or
    whether it wants any printed at all.
    """

    def __init__(self, core_obj: Any, opts=None):
        self.core = core_obj
        self.debugger = core_obj.debugger
        return

    # FIXME: remove byteName and arguments and have the last instruction sent back
    def event_hook(
        self,
        event: str,
        offset: int,
        byteName: str,
        byteCode: int,
        line_number: int,
        intArg: Optional[int],
        event_arg: Any,
        vm: Any,
        prompt="trepan-xpy-trace",
    ) -> Optional[Callable]:
        "A simple event processor that prints out events."
        if vm.frame:
            if offset >= 0:
                print("%-12s - %s" % (event,
                                      format_instruction_with_highlight(
                                          vm.frame,
                                          vm.opc,
                                          byteName,
                                          intArg,
                                          event_arg,
                                          offset,
                                          line_number,
                                          extra_debug=False,
                                          settings=self.debugger.settings,
                                          show_line=True,
                                          vm=vm
                                      )))
            else:
                frame = vm.frame
                lineno = frame.line_number()
                filename = self.core.canonic_filename(frame)
                filename = self.core.filename(filename)
                print("%s - %s:%d" % (event, filename, lineno))
        else:
                print("%s" % (event,))

        return self.event_hook

    pass
