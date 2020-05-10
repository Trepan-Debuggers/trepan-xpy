# -*- coding: utf-8 -*-
# This file is stripped down from the one in trepan3k
#
#   Copyright (C) 2008-2010, 2013-2020 Rocky Bernstein <rocky@gnu.org>
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
import linecache, sys, re
import pyficache

from typing import Any

# Note: the module name pre 3.2 is repr
from reprlib import Repr

from pygments.console import colorize

from trepanxpy.processor.trace import EVENT2SHORT

import trepan.lib.bytecode as Mbytecode
import trepan.lib.display as Mdisplay
import trepan.lib.thred as Mthread
import trepan.processor.complete as Mcomplete

from trepan.processor.cmdproc import (
    CommandProcessor,
    arg_split,
    resolve_name,
    print_location,
)

warned_file_mismatches = set()


# Default settings for command processor method call
DEFAULT_PROC_OPTS = {
    # A list of debugger initialization files to read on first command
    # loop entry.  Often this something like [~/.config/trepan-xp/profile] which the
    # front-end sets.
    "initfile_list": []
}

# FIXME: can't figure out how to delegate specific fns so we'll subclass instead.
class XPyCommandProcessor(CommandProcessor):
    def __init__(self, core_obj, opts=None):
        super().__init__(core_obj, opts)
        self.core = core_obj
        self.debugger = core_obj.debugger

        self.continue_running = False  # True if we should leave command loop
        self.event2short = dict(EVENT2SHORT)
        self.event2short["signal"] = "?!"
        self.event2short["brkpt"] = "xx"

        self.optional_modules = ()

        # command argument string. Is like current_command, but the part
        # after cmd_name has been removed.
        self.cmd_argstr = ""

        # command name before alias or macro resolution
        self.cmd_name = ""
        self.cmd_queue = []  # Queued debugger commands
        self.completer = lambda text, state: Mcomplete.completer(self, text, state)
        self.current_command = ""  # Current command getting run
        self.debug_nest = 1
        self.display_mgr = Mdisplay.DisplayMgr()
        self.intf = core_obj.debugger.intf
        self.last_command = None  # Initially a no-op
        self.precmd_hooks = []

        self.location = lambda: print_location(self)

        self.preloop_hooks = []
        self.postcmd_hooks = []

        # Note: prompt_str's value set below isn't used. It is
        # computed dynamically. The value is suggestive of what it
        # looks like.
        self.prompt_str = "(trepan-xpy) "

        # Stop only if line/file is different from last time
        self.different_line = None

        # These values updated on entry. Set initial values.
        self.curframe = None
        self.event = None
        self.event_arg = None
        self.frame = None
        self.list_lineno = 0  # last list number used in "list"
        self.list_offset = -1  # last list number used in "disassemble"
        self.list_obj = None
        self.list_filename = None  # last filename used in list
        self.list_orig_lineno = 0  # line number of frame or exception on setup
        self.list_filename = None  # filename of frame or exception on setup

        self.macros = {}  # Debugger Macros

        # Create a custom safe Repr instance and increase its maxstring.
        # The default of 30 truncates error messages too easily.
        self._repr = Repr()
        self._repr.maxstring = 100
        self._repr.maxother = 60
        self._repr.maxset = 10
        self._repr.maxfrozen = 10
        self._repr.array = 10
        self.stack = []
        self.thread_name = None
        self.frame_thread_name = None

        # initfile_list = get_option("initfile_list")
        # for init_cmdfile in initfile_list:
        #     self.queue_startfile(init_cmdfile)


        # FIXME: This doesn't work
        # # Delegate functions here:
        # self.cmdproc = CommandProcessor(self)
        # for method in (
        #         "_saferepr",
        #         "add_preloop_hook",
        #         "defaultFile",
        #         "eval",
        #         "exec_line",
        #         "forget",
        #         "get_an_int",
        #         "get_int_noerr",
        #         "getval",
        #         "ok_for_running",
        #         "process_commands",
        #         "queue_startfile",
        #         "remove_preloop_hook",
        #         "setup",
        #         "undefined_cmd",
        #         "read_history_file",
        #         "write_history_file",
        #         ):
        #     setattr(self, method, getattr(cmdproc, method))

        self.cmd_instances = self._populate_additional_commands()
        # self._populate_cmd_lists(cmdproc)

        return

    def set_prompt(self, prompt="trepan-xpy"):
        if self.thread_name and self.thread_name != "MainThread":
            prompt += ":" + self.thread_name
            pass
        self.prompt_str = "%s%s%s" % (
            "(" * self.debug_nest,
            prompt,
            ")" * self.debug_nest,
        )
        highlight = self.debugger.settings["highlight"]
        if highlight and highlight in ("light", "dark"):
            self.prompt_str = colorize("underline", self.prompt_str)
        self.prompt_str += " "

    def event_hook(self,
                   event: str,
                   offset: int,
                   byteName: str,
                   event_arg: Any,
                   vm: Any, prompt="trepan-xpy"):
        "command event processor: reading a commands do something with them."
        self.vm = vm
        self.frame = vm.frame
        self.event = event
        self.event_arg = event_arg

        filename = self.frame.f_code.co_filename
        lineno = self.frame.f_lineno
        line = linecache.getline(filename, lineno, self.frame.f_globals)
        if not line:
            opts = {
                "output": "plain",
                "reload_on_change": self.settings("reload"),
                "strip_nl": False,
            }
            m = re.search("^<frozen (.*)>", filename)
            if m and m.group(1):
                filename = pyficache.unmap_file(m.group(1))
            line = pyficache.getline(filename, lineno, opts)
        self.current_source_text = line
        if self.settings("skip") is not None:
            if Mbytecode.is_def_stmt(line, self.frame):
                return True
            if Mbytecode.is_class_def(line, self.frame):
                return True
            pass
        self.thread_name = Mthread.current_thread_name()
        self.frame_thread_name = self.thread_name
        self.set_prompt(prompt)
        self.process_commands()
        if filename == "<string>":
            pyficache.remove_remap_file("<string>")
        return True

    def _populate_additional_commands(self):
        """ Create an instance of each of the debugger
        commands. Commands are found by importing files in the
        directory 'command'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""
        # FIXME: Fill on when we have additional commands like stepi
        return

    def setup(self):
        """Initialization done before entering the debugger-command
        loop. In particular we set up the call stack used for local
        variable lookup and frame/up/down commands.

        We return True if we should NOT enter the debugger-command
        loop."""
        self.forget()
        if self.event in ["exception", "c_exception"]:
            exc_type, exc_value, exc_traceback = self.event_arg
        else:
            _, _, exc_traceback = (
                None,
                None,
                None,
            )  # NOQA
            pass
        self.curindex = 0
        if self.frame or exc_traceback:
            stack = self.vm.frame.stack
            if stack == []:
                # FIXME: Just starting up - should there be an event for this
                # Or do we need to do this for all call events?
                stack = [self.frame]
            self.stack = [(frame, frame.line_number()) for frame in stack]
            self.curframe = self.frame
            # FIXME
            # self.thread_name = Mthread.current_thread_name()
            self.thread_name = "Main"
            if exc_traceback:
                self.list_lineno = self.frame.line_number()
                self.list_offset = self.curframe.f_lasti
                self.list_object = self.curframe
        else:
            self.stack = self.curframe = self.botframe = None
            pass
        if self.curframe:
            self.list_lineno = self.frame.line_number()
            self.list_offset = self.curframe.f_lasti
            self.list_filename = self.curframe.f_code.co_filename
            self.list_object = self.curframe
        else:
            self.list_object = None
            if not exc_traceback:
                self.list_lineno = None
            pass
        # if self.execRcLines()==1: return True

        # FIXME:  do we want to save self.list_lineno a second place
        # so that we can do 'list .' and go back to the first place we listed?
        return False


# Demo it
if __name__ == "__main__":
    from trepan.processor.command import mock as Mmock

    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    print("commands:")
    commands = list(cmdproc.commands.keys())
    commands.sort()
    print(commands)
    print("aliases:")
    aliases = list(cmdproc.aliases.keys())
    aliases.sort()
    print(aliases)
    print(resolve_name(cmdproc, "quit"))
    print(resolve_name(cmdproc, "q"))
    print(resolve_name(cmdproc, "info"))
    print(resolve_name(cmdproc, "i"))
    # print '-' * 10
    # print_source_line(sys.stdout.write, 100, 'source_line_test.py')
    # print '-' * 10
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    print()
    print("-" * 10)
    cmdproc.location()
    print("-" * 10)
    print(cmdproc.eval("1+2"))
    print(cmdproc.eval("len(aliases)"))
    import pprint

    print(pprint.pformat(cmdproc.category))
    print(arg_split("Now is the time"))
    print(arg_split("Now is the time ;;"))
    print(arg_split("Now is 'the time'"))
    print(arg_split("Now is the time ;; for all good men"))
    print(arg_split("Now is the time ';;' for all good men"))

    print(cmdproc.commands)
    fn = cmdproc.commands["quit"]

    print("Removing non-existing quit hook: %s" % cmdproc.remove_preloop_hook(fn))
    cmdproc.add_preloop_hook(fn)
    print(cmdproc.preloop_hooks)
    print("Removed existing quit hook: %s" % cmdproc.remove_preloop_hook(fn))
    pass
