# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>

from typing import List
import os
import sys
from xpython.execfile import run_python_file, NoSourceError

# Default settings used here
from trepan.lib.default import DEBUGGER_SETTINGS
import trepan.interfaces.user as Muser
import trepan.misc as Mmisc
from trepan.exception import DebuggerQuit, DebuggerRestart

from trepanxpy.core import TrepanXPyCore
# from trepanxpy.processor.trace import XPyPrintProcessor
from trepanxpy.processor.cmd import XPyCommandProcessor


class Debugger(object):
    def __init__(self, path: str, args: List[str]):
        """Create a debugger object. But depending on the value of
        key 'start' inside hash 'opts', we may or may not initially
        start debugging.

        See also Debugger.start and Debugger.stop.
        """

        self.mainpyfile  = None
        self.thread      = None

        completer  = lambda text, state: self.complete(text, state)
        interface_opts={
            "complete": completer,
            "debugger_name": "trepan-xpy",
        }
        interface = Muser.UserInterface(opts=interface_opts)
        self.intf = [interface]

        # main_dirname is the directory where the script resides.
        # Filenames in co_filename are often relative to this.
        self.main_dirname = os.curdir

        self.filename_cache = {}
        self.settings = DEBUGGER_SETTINGS
        self.core = TrepanXPyCore(self, {})
        # processor = XPyPrintProcessor(self.core, self)
        processor = XPyCommandProcessor(self.core, self)
        self.callback_hook = processor.event_hook

        # Save information for restarting
        mainpyfile = self.core.canonic(path)
        self.program_sys_argv = None
        self.orig_sys_argv = list(sys.argv)

        if path:
            while True:
                print("Running x-python %s with %s" % (path, args))
                try:
                    run_python_file(path, args, callback=self.callback_hook)
                except DebuggerQuit:
                    break
                except DebuggerRestart:
                    self.core.execution_status = "Restart requested"
                    if self.program_sys_argv:
                        sys.argv = list(self.program_sys_argv)
                        part1 = "Restarting %s with arguments:" % self.core.filename(mainpyfile)
                        args = " ".join(self.program_sys_argv[1:])
                        self.intf[-1].msg(
                            Mmisc.wrapped_lines(part1, args, self.settings["width"])
                        )
                    else:
                        break
                except (FileNotFoundError, NoSourceError) as e:
                    self.intf[-1].msg(str(e))
                    sys.exit(1)
                except SystemExit:
                    # In most cases SystemExit does not warrant a post-mortem session.
                    break

        else:
            print("Hi, rocky!, you typed: path: %s, args: %s" % (path, args))

    def restart_argv(self):
        '''Return an array that would be execv-ed  to restart the program'''
        return self.orig_sys_argv or self.program_sys_argv
