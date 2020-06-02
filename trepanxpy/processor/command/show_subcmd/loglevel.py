# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2015, 2020 Rocky Bernstein
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

from xpython.vm import log
from trepan.processor.command.base_subcmd import DebuggerSubcommand

LOGLEVEL2NAME = {
    50: "critical",
    40: "error",
    30: "warning",
    20: "info",
    10: "debug",
    00: "notset"
}


class ShowLogLevel(DebuggerSubcommand):
    """**show loglevel**

Show VM logger log level setting.

See also:
---------

`set logtrace`"""

    min_abbrev = len("logl")
    short_help = "Show VM logger log level setting"
    pass

    def run(self, args):
        if len(args) != 0:
            self.errmsg("Expecting no args")
            return

        log_str = LOGLEVEL2NAME.get(log.getEffectiveLevel(), "unknown")
        self.msg("PyVM log level is %s" % log_str)
        return
    pass

if __name__ == "__main__":
    # from trepan.processor.command.show_subcmd.__demo_helper__ import demo_run

    # demo_run(ShowLogLevel)
    pass
