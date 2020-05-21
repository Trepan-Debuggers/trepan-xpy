# -*- coding: utf-8 -*-
#  Copyright (C) 2009-2010, 2013, 2015, 2017, 2020 Rocky Bernstein
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
import code, os.path as osp, sys

# Our local modules
from trepan.processor.command.python import (
    PythonCommand as Trepan3kShell,
    interact,
    runcode,
)
from trepan.interfaces.server import ServerInterface


class PythonCommand(Trepan3kShell):
    """**python**

Run Python as a command subshell. The *sys.ps1* prompt will be set to
`trepan-xpy >>> `.

To issue a debugger command use function *dbgr()*. For example:

  dbgr('info program')

The current call frame and Interpreter VM access is available through variables: frame, and vm.
"""

    aliases = ("py", "shell")
    category = "support"
    min_args = 0
    max_args = 1
    name = osp.basename(__file__).split(".")[0]
    need_stack = False
    short_help = "Run a Python interactive shell"

    def run(self, args):
        # See if python's code module is around

        # Python does it's own history thing.
        # Make sure it doesn't damage ours.
        intf = self.debugger.intf[-1]
        if isinstance(intf, ServerInterface):
            self.errmsg("Can't run an interactive shell on a remote session")
            return

        have_line_edit = self.debugger.intf[-1].input.line_edit
        if have_line_edit:
            try:
                self.proc.write_history_file()
            except IOError:
                pass
            pass

        banner_tmpl = """trepan-xpy python shell%s
Use dbgr(*string*) to issue debugger command: *string*"""

        banner_tmpl += "\nVariable 'frame' contains the current frame; 'vm', the current vm object."

        my_locals = {}
        my_globals = None
        proc = self.proc
        if proc.curframe:
            my_globals = proc.curframe.f_globals
            if self.proc.curframe.f_locals:
                my_locals = proc.curframe.f_locals
                pass
            pass

        # Give the user a way to get access frame, vm and debugger commands
        my_locals["vm"] = proc.vm
        my_locals["frame"] = proc.frame
        my_locals["dbgr"] = self.dbgr

        # Change from debugger completion to python completion
        try:
            import readline
        except ImportError:
            pass
        else:
            readline.parse_and_bind("tab: complete")

        sys.ps1 = "trepan-xpy >>> "
        old_sys_excepthook = sys.excepthook
        try:
            sys.excepthook = None
            if len(my_locals):
                interact(
                    banner=(banner_tmpl % " with locals"),
                    my_locals=my_locals,
                    my_globals=my_globals,
                )
            else:
                interact(banner=(banner_tmpl % ""))
                pass
        finally:
            sys.excepthook = old_sys_excepthook

        # restore completion and our history if we can do so.
        if hasattr(self.proc.intf[-1], "complete"):
            try:
                from readline import set_completer, parse_and_bind

                parse_and_bind("tab: complete")
                set_completer(self.proc.intf[-1].complete)
            except ImportError:
                pass
            pass

        if have_line_edit:
            self.proc.read_history_file()
            pass
        return

    pass


if __name__ == "__main__":
    from trepanxpy.debugger import Debugger

    d = Debugger("x + 1", is_file=False, trace_only=False, args=[])
    command = PythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print("Type Python commands and exit to quit.")
        print(sys.argv[1])
        if sys.argv[1] == "-d":
            print(command.run(["python", "-d"]))
        else:
            print(command.run(["python"]))
            pass
        pass
    pass
