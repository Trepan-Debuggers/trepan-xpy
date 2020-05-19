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

from getopt import getopt, GetoptError

from trepan.processor.command.base_subcmd import DebuggerSubcommand
from trepan.processor.cmdfns import get_an_int
from trepan.misc import wrapped_lines


class SetPC(DebuggerSubcommand):
    """**set pc** [ *flag* ] *line-or-offset*

Set the PC to run at *line-or-offset*

*flag* can be one of:

* `--offset` | `-o` to indicate an offset
* `--line` | `-l` to indicate a line number
* `=` which is ignored. It is syntactic sugar

Alternatively, the line-or-offset can be indicated by prefixing the
number with `l` or `@` respectively.

Examples
--------

    set pc 0
    set pc @0            # same as above
    set pc --offset 0    # same as above
    set pc -o 0          # same as above
    set pc = 0           # same as above

    set pc l2            # same as above
    set pc --line 2      # same as above
    set pc -l 2          # same as above
    set pc = l0          # same as above

See Also
--------

`info pc`
"""

    in_list    = True
    min_abbrev = len('pc')
    max_args = 2
    need_stack = True
    short_help = "Set Program Counter"

    def run(self, args):
        mainfile = self.core.filename(None)
        if self.core.is_running():
            proc = self.proc

            is_offset = True
            n = len(args)
            if n == 2:
                if args[0] == "=":
                    args[0] = args[1]
                else:
                    try:
                        opts, args = getopt(args, "hlo",
                                            ["help", "line", "offset"])
                    except GetoptError as err:
                        # print help information and exit:
                        print(str(err))  # will print something like "option -a not recognized"
                        return

                    for o, a in opts:
                        if o in ("-h", "--help"):
                            proc.commands["help"].run(["help", "set", "pc"])
                            return
                        elif o in ("-l", "--line", ):
                            is_offset = False
                        elif o in ("-o", "--offset"):
                            is_offset = True
                        else:
                            self.errmsg("unhandled option '%s'" % o)
                        pass
                    pass
                pass

            frame = proc.frame
            if frame:
                code = frame.f_code
                if is_offset:
                    min_value = 0
                    max_value = len(code.co_code) - 1
                elif len(code.co_lnotab) > 0:
                    min_value = code.co_firstlineno
                    # FIXME: put this in a function in xdis somewhere.
                    # Also: won't need ord() in Python 2.x
                    # max_value = min_value + sum([ord(i) for i in code.co_lnotab[1::2]])
                    max_value = min_value + sum(code.co_lnotab[1::2])
                else:
                    min_value = max_value = code.co_firstline

                offset = get_an_int(
                    self.errmsg,
                    args[0],
                    "The 'pc' command requires an integer offset or a line.",
                    min_value, max_value,
                )
                if offset is None:
                    return None
                # FIXME: We check that offset points to an
                # opcode or a valid line as opposed to an operand
                if not is_offset:
                    self.errmsg("Sorry, line numbers not handled right now.")
                    return None

                self.list_offset = frame.f_lasti = offset
                frame.fallthrough = False
                self.list_lineno = frame.f_lineno = frame.line_number()
                self.msg("Execution set to resume at offset %d" % offset)
                self.return_status = "skip"
                return None
            else:
                self.errmsg("Oddly, a frame is not set - nothing done.")
                pass
        else:
            if mainfile:
                part1 = "Python program '%s'" % mainfile
                msg = "is not currently running. "
                self.msg(wrapped_lines(part1, msg, self.settings["width"]))
            else:
                self.msg("No Python program is currently running.")
                pass
            self.msg(self.core.execution_status)
            pass
        return None

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run

    demo_run(SetPC, [0])
    pass
