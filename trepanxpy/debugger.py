# -*- coding: utf-8 -*-
#   Copyright (C) 2020 Rocky Bernstein <rocky@gnu.org>

from typing import List, Dict, Any
import os
import sys
from xpython.execfile import run_python_file, run_python_string, NoSourceError

# Default settings used here
from trepanxpy.debugger_defaults import DEBUGGER_SETTINGS
from trepan.interfaces.user import UserInterface
from trepan.misc import wrapped_lines
from trepan.exception import DebuggerQuit, DebuggerRestart

from trepanxpy.core import TrepanXPyCore
from trepanxpy.fmt import format_instruction_with_highlight
from trepanxpy.processor.cmd import XPyCommandProcessor
from trepanxpy.processor.trace import XPyPrintProcessor


class TrepanXPy(object):
    def __init__(
        self, string_or_path: str, is_file: bool, trace_only: bool, args: List[str]
    ):
        """Create a debugger object. But depending on the value of
        key 'start' inside hash 'opts', we may or may not initially
        start debugging.

        See also TrepanXPy.start and TrepanXPy.stop.
        """

        def instruction_fmt_func(frame, opc, byte_name, int_arg, arguments, offset, line_number,
                                 extra_debug, vm):
            return format_instruction_with_highlight(
                frame=frame,
                opc=opc,
                byte_name=byte_name,
                int_arg = int_arg,
                arguments = arguments,
                offset = offset,
                line_number = line_number,
                extra_debug = extra_debug,
                settings=self.settings,
                vm = vm,
                show_line = True
            )

        self.mainpyfile = None
        self.thread = None

        completer = lambda text, state: self.complete(text, state)
        interface_opts = {
            "complete": completer,
            "debugger_name": "trepan-xpy",
        }
        interface = UserInterface(opts=interface_opts)
        self.intf = [interface]

        # main_dirname is the directory where the script resides.
        # Filenames in co_filename are often relative to this.
        self.main_dirname = os.curdir

        self.filename_cache: Dict[str, Any] = {}
        self.settings = DEBUGGER_SETTINGS
        self.core = TrepanXPyCore(self, {})
        if trace_only:
            processor = XPyPrintProcessor(self.core)
        else:
            processor = XPyCommandProcessor(self.core)
        self.core.processor = processor
        self.callback_hook = self.core.trace_dispatch

        # Save information for restarting
        self.program_sys_argv = list(sys.argv)
        self.orig_sys_argv = list(sys.argv)

        if is_file:
            mainpyfile = self.core.canonic(string_or_path)
            run_fn = run_python_file
        else:
            mainpyfile = string_or_path
            run_fn = run_python_string

        while True:
            print("Running x-python %s with %s" % (string_or_path, args))
            try:
                run_fn(
                    string_or_path,
                    args,
                    callback=self.callback_hook,
                    format_instruction=instruction_fmt_func,
                )
            except DebuggerQuit:
                break
            except DebuggerRestart:
                self.core.execution_status = "Restart requested"
                if self.program_sys_argv:
                    sys.argv = list(self.program_sys_argv)
                    part1 = "Restarting %s with arguments:" % self.core.filename(
                        mainpyfile
                    )
                    args = " ".join(self.program_sys_argv[1:])
                    self.intf[-1].msg(
                        wrapped_lines(part1, args, self.settings["width"])
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
                if trace_only:
                    break
                msg = "The program finished - press enter to restart; anything else terminates. ? "
                response = input(msg)
                if response != "":
                    break
                pass

    def restart_argv(self):
        """Return an array that would be execv-ed  to restart the program"""
        return self.orig_sys_argv or self.program_sys_argv
