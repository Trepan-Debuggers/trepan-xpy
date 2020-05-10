# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>

from typing import List
import os
from xpython.execfile import run_python_file

# Default settings used here
from trepan.lib.default import DEBUGGER_SETTINGS
import trepan.interfaces.user as Muser

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

        completer  = lambda text, state: self.complete(text, state)
        interface_opts={'complete': completer}
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

        if path:
            print("Running x-python %s with %s" % (path, args))

            run_python_file(path, args, callback=self.callback_hook)
        else:
            print("Hi, rocky!, you typed: path: %s, args: %s" % (path, args))
