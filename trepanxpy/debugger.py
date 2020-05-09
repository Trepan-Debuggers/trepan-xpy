# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>

import os
import os.path as osp
from typing import List
from trepanxpy.clifns import search_file
from xpython.execfile import run_python_file

DEFAULT_SETTINGS = {"basename": False}


class Debugger(object):
    def __init__(self, path: str, args: List[str]):

        # main_dirname is the directory where the script resides.
        # Filenames in co_filename are often relative to this.
        self.main_dirname = os.curdir

        self.filename_cache = {}
        self.settings = DEFAULT_SETTINGS

        if path:
            print("Running x-python %s with %s" % (path, args))
            import logging
            logging.basicConfig(level=logging.INFO)
            run_python_file(path, args)
        else:
            print("Hi, rocky!, you typed: path: %s, args: %s" % (path, args))


    def canonic(self, filename: str) -> str:
        """ Turns `filename' into its canonic representation and returns this
        string. This allows a user to refer to a given file in one of several
        equivalent ways.

        Relative filenames need to be fully resolved, since the current working
        directory might change over the course of execution.

        If filename is enclosed in < ... >, then we assume it is
        one of the bogus internal Python names like <string> which is seen
        for example when executing "exec cmd".
        """
        if filename == "<" + filename[1:-1] + ">":
            return filename
        canonic = self.filename_cache.get(filename)
        if not canonic:
            lead_dir = filename.split(os.sep)[0]
            if lead_dir == os.curdir or lead_dir == os.pardir:
                # We may have invoked the program from a directory
                # other than where the program resides. filename is
                # relative to where the program resides. So make sure
                # to use that.
                canonic = osp.abspath(osp.join(self.main_dirname, filename))
            else:
                canonic = osp.abspath(filename)
                pass
            if not osp.isfile(canonic):
                canonic = search_file(filename, self.search_path, self.main_dirname)
                # FIXME: is this is right for utter failure?
                if not canonic:
                    canonic = filename
                pass
            canonic = osp.realpath(osp.normcase(canonic))
            self.filename_cache[filename] = canonic
        return canonic

    def canonic_filename(self, frame) -> str:
        """Picks out the file name from `frame' and returns its
         canonic() value, a string."""
        return self.canonic(frame.f_code.co_filename)

    def filename(self, filename=None) -> str:
        """Return filename or the basename of that depending on the
        basename setting"""
        if filename is None:
            if self.debugger.mainpyfile:
                filename = self.debugger.mainpyfile
            else:
                return None
        if self.settings["basename"]:
            return osp.basename(filename)
        return filename
