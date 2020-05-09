# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>

from typing import List
import os
from xpython.execfile import run_python_file

from trepanxpy.lib.core import TrepanXPyCore
from trepanxpy.processor.trace import PrintProcessor


DEFAULT_SETTINGS = {"basename": False}


class Debugger(object):
    def __init__(self, path: str, args: List[str]):

        # main_dirname is the directory where the script resides.
        # Filenames in co_filename are often relative to this.
        self.main_dirname = os.curdir

        self.filename_cache = {}
        self.settings = DEFAULT_SETTINGS
        self.core = TrepanXPyCore(self, {})
        processor = PrintProcessor(self.core, self)
        self.callback_hook = processor.event_hook

        if path:
            print("Running x-python %s with %s" % (path, args))

            run_python_file(path, args, callback=self.callback_hook)
        else:
            print("Hi, rocky!, you typed: path: %s, args: %s" % (path, args))
