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
    """**set logtrace** [ **on** | **off** | **debug** | **info** ]

Show logtrace PyVM logger messages. Initially logtracing is `off`.

However running `set logtrace` will turn it on and set the log level to `debug`. So it's the
same thing as `set logtrace debug`.

If you want the less verbose messages, use `info`. And to turn off,
(except critical errors), use `off`.

Examples:
---------

     set logtrace         # turns x-python on info logging messages
     set logtrace info    # same as above
     set logtrace debug   # turn on info and debug logging messages
     set logtrace off     # turn off all logging messages except critical ones
    """

    in_list    = True
    min_abbrev = len('lo')

    logger_choices = frozenset(["debug", "info", "off", "on"])

    def complete(self, prefix):
        return complete_token(SetLogTrace.logger_choices, prefix)

    def get_logtrace_level(self, arg):
        if not arg: return "info"
        if arg in SetLogTrace.logger_choices:
            return arg
        else:
            self.errmsg('Expecting %s"; got %s' %
                        (', '.join(SetLogtrace.highlight_choices), arg))
            return None
        pass


    def run(self, args):
        if len(args) == 0:
            logtrace_level = logging.INFO
        else:
            level_str = self.get_logtrace_level(args[0])
            if not level_str:
                return
            if level_str == "off":
                logtrace_level = logging.CRITICAL
            elif level_str in ("info", "on") :
                logtrace_level = logging.INFO
            else:
                assert level_str == "debug"
                logtrace_level = logging.DEBUG
            print("XXX", level_str, logtrace_level)
            pass
        self.debugger.settings[self.name] = logtrace_level
        logging.basicConfig(level=logtrace_level)
        return

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run
    demo_run(SetLogTrace, [])
    pass
