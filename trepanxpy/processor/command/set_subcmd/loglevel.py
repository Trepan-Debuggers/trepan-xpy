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

from trepan.processor.command.base_subcmd import DebuggerSubcommand
from trepan.lib.complete import complete_token


class SetLogLevel(DebuggerSubcommand):
    """**set loglevel** [ **on** | **off** | **debug** | **info** | **critical* | *warn* ]

Show loglevel PyVM logger messages. Initially logtracing is `off`.

However running `set loglevel` will turn it on and set the log level to `debug`. So it's the
same thing as `set loglevel debug`.

If you want the less verbose messages, use `info`. And to turn off,
(except critical errors), use `off`.

Examples:
---------

     set loglevel         # turns x-python on info logging messages
     set loglevel info    # same as above
     set loglevel debug   # turn on info and debug logging messages
     set loglevel off     # turn off all logging messages except critical ones
    """

    in_list    = True
    min_abbrev = len('logl')

    logger_choices = frozenset(["debug", "info", "warn", "warning", "critical", "off", "on"])

    def complete(self, prefix):
        return complete_token(SetLogLevel.logger_choices, prefix)

    def get_loglevel_level(self, arg):
        if not arg: return "info"
        if arg in SetLogLevel.logger_choices:
            return arg
        else:
            self.errmsg('Expecting %s"; got %s' %
                        (', '.join(SetLogLevel.logger_choices), arg))
            return None
        pass


    def run(self, args):
        if len(args) == 0:
            loglevel_level = logging.INFO
        else:
            level_str = self.get_loglevel_level(args[0])
            if not level_str:
                return
            if level_str in ("off", "critical"):
                loglevel_level = logging.CRITICAL
            elif level_str in ("info", "on") :
                loglevel_level = logging.INFO
            elif level_str in ("warn", "warning") :
                loglevel_level = logging.WARNING
            else:
                assert level_str == "debug"
                loglevel_level = logging.DEBUG
            pass

        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
            pass
        logging.basicConfig(level=loglevel_level)
        self.proc.commands["show"].run(["show", "loglevel"])
        return

    pass

if __name__ == '__main__':
    from trepan.processor.command.set_subcmd.__demo_helper__ import demo_run
    demo_run(SetLogLevel, [])
    pass
