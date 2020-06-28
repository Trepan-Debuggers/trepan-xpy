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
import linecache, sys, re, inspect
import importlib
import pyficache
import os.path as osp

from typing import Any, Optional, Set

# Note: the module name pre 3.2 is repr
from reprlib import Repr

from pygments.console import colorize

import trepan.lib.bytecode as Mbytecode
import trepan.lib.display as Mdisplay
from trepan.misc import option_set
from trepan.lib.thred import current_thread_name
import trepan.processor.complete as Mcomplete

from trepan.processor.cmdproc import (
    CommandProcessor,
    arg_split,
    resolve_name,
    print_location,
)

from trepanxpy.events import EVENT2SHORT
from trepanxpy.fmt import format_instruction_with_highlight


warned_file_mismatches: Set[str] = set()


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


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

        # FIXME: can we adjust this to also show the instruction?
        self.location = lambda: self

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

        get_option = lambda key: option_set(opts, key, DEFAULT_PROC_OPTS)
        initfile_list = get_option("initfile_list")
        for init_cmdfile in initfile_list:
            self.queue_startfile(init_cmdfile)

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

        # Remove trepan3k commands which aren't valid here, and those specific to trepan-xpy
        remove_commands = (
            "continue",
            "finish",
            "next",
            "quit",
            "set",
            "step",
        )
        new_instances = []
        for cmd in self.cmd_instances:
            if cmd.name in remove_commands:
                del self.commands[cmd.name]
            else:
                new_instances.append(cmd)
                pass
            pass
        self.cmd_instances = new_instances

        new_commands = self._update_commands()
        for new_command in new_commands:
            self.commands[new_command.name] = new_command
        self.cmd_instances += new_commands
        self._populate_cmd_lists()

        if self.debugger.settings["autopc"]:
            self.commands["set"].run(["set", "autopc"])
        return

    def update_commands_easy_install(self, Mcommand):
        """
        Add files in filesystem to self.commands.
        If running from source or from an easy_install'd package, this is used.
        """
        cmd_instances = []

        for mod_name in Mcommand.__modules__:
            if mod_name in ("info_sub", "set_sub", "show_sub",):
                pass
            import_name = "%s.%s" % (Mcommand.__name__, mod_name)
            try:
                command_mod = importlib.import_module(import_name)
            except:
                if mod_name not in self.optional_modules:
                    print("Error importing %s: %s" % (mod_name, sys.exc_info()[0]))
                    pass
                continue

            classnames = [
                tup[0]
                for tup in inspect.getmembers(command_mod, inspect.isclass)
                if (
                    tup[0] != "DebuggerCommand"
                    and not tup[0].startswith("Trepan3k")
                    and tup[0].endswith("Command")
                )
            ]
            for classname in classnames:
                if False:
                    instance = getattr(command_mod, classname)(self)
                    cmd_instances.append(instance)
                else:
                    try:
                        instance = getattr(command_mod, classname)(self)
                        cmd_instances.append(instance)
                    except:
                        print(
                            "Error loading %s from %s: %s"
                            % (classname, mod_name, sys.exc_info()[0])
                        )
                        pass
                    pass
                pass
            pass
        return cmd_instances

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

    def event_hook(
        self,
        event: str,
        offset: int,
        byteName: str,
        byteCode: int,
        line_number: int,
        intArg: Optional[int],
        event_arg: Any,
        vm: Any,
        prompt="trepan-xpy",
    ):
        "command event processor: reading a commands do something with them."

        def frame_setup(frame):
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            line = linecache.getline(filename, lineno, frame.f_globals)
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
            return line, filename

        self.vm = vm
        self.frame = vm.frame
        self.event = event
        self.event_arg = event_arg

        # In order to follow Python's sys.settrace()'s convention:
        # returning "None" turns off tracing for the scope.
        # However we do not need to return a reference to ourself,
        # a callable (this may be allowed in the future though).
        # Instead for now a string status is returned
        # * "skip" for skip next instruction, and
        # * "return" for immediate return
        # * "finish" for "step out"

        self.return_status = True

        if event == "fatal":
            self.core.execution_status = "Terminated"
            # One last hurrah!

            tb = vm.last_traceback
            if tb:
                frame_setup(tb.tb_frame)
                self.vm.frames = []
                while tb:
                    self.vm.frames.insert(0, tb.tb_frame)
                    tb = tb.tb_next
                self.curframe = self.frame = self.vm.frames[0]
                self.setup()
                self.curindex = len(vm.frames) - 1
                print_location(self)

            self.set_prompt("trepan-xpy:pm")
            self.process_commands()
            return None

        if self.vm.frame:
            self.core.execution_status = "Running"
        else:
            self.core.execution_status = "Terminated"
            return

        line, filename = frame_setup(self.frame)
        if self.settings("skip"):
            # Note that in contrast to skipping intructions
            # when return_status is set to "skip", here
            # we are execution the instruction but just skipping
            # any handling this instruction the debugger.
            if Mbytecode.is_def_stmt(line, self.frame):
                return self
            if Mbytecode.is_class_def(line, self.frame):
                return
            pass
        self.thread_name = current_thread_name()
        self.frame_thread_name = self.thread_name

        self.setup()
        print_location(self)
        if offset >= 0 and event not in ('call', 'return'):
            self.msg(
                "%s"
                % format_instruction_with_highlight(
                    vm.frame,
                    vm.opc,
                    byteName,
                    intArg,
                    event_arg,
                    offset,
                    line_number,
                    extra_debug=False,
                    settings=self.debugger.settings,
                    show_line=False,  # We show the line number in our location reporting
                    vm=self.vm,
                    repr=self._repr.repr
                )
            )

        self.set_prompt(prompt)
        self.process_commands()
        if filename == "<string>":
            pyficache.remove_remap_file("<string>")
        return self.return_status

    def _update_commands(self):
        """ Create an instance of each of the debugger
        commands. Commands are found by importing files in the
        directory 'command'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""
        from trepanxpy.processor import command as Mcommand

        if hasattr(Mcommand, "__modules__"):
            # This is also used when installing from source
            return self.update_commands_easy_install(Mcommand)
        else:
            return self.populate_commands_pip(Mcommand, "trepanxpy")

    def setup(self):
        """Initialization done before entering the debugger-command
        loop. In particular we set up the call stack used for local
        variable lookup and frame/up/down commands.

        We return True if we should NOT enter the debugger-command
        loop."""
        self.forget()
        self.curindex = 0
        if self.vm.frames:
            stack = self.vm.frames
            if stack == []:
                # FIXME: Just starting up - should there be an event for this
                # Or do we need to do this for all call events?
                stack = [self.frame]
                pass
            self.stack = [(frame, frame.line_number()) for frame in reversed(stack)]
            self.curframe = self.frame
            self.thread_name = "MainThread"
        else:
            self.stack = self.curframe = self.botframe = None
            pass
        if self.curframe:
            self.list_lineno = (
                max(
                    1,
                    self.frame.line_number()
                    - int(self.settings("listsize") / 2),
                )
                - 1
            )
            self.list_offset = self.curframe.f_lasti
            self.list_filename = self.curframe.f_code.co_filename
            self.list_object = self.curframe
        else:
            self.list_object = None
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
