# -*- coding: utf-8 -*-
#  Copyright (C) 2009, 2013, 2015, 2020 Rocky Bernstein
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
import os.path as osp

from xpython.vmtrace import PyVMEVENT_ALL

from trepan.processor.command.base_cmd import DebuggerCommand

# Our local modules

class StepICommand(DebuggerCommand):
    """**stepi** [*count*]

Step an instruction, stopping at the next instruction or event.

With an integer argument, step that many times.


Examples:
---------

  stepi        # step 1 event, *any* event
  stepi 1      # same as above
  stepi 5/5+0  # same as above

Related and similar is the `next` command. More general is the `step` command

See also:
---------

`step` `next`, `skip`, `jump` (there's no `hop` yet), `continue`, `return` and
`finish` for other ways to progress execution.
"""

    aliases       = ('si',)
    category      = 'running'
    min_args      = 0
    max_args      = None
    execution_set = ['Running']
    name          = osp.basename(__file__).split('.')[0]
    need_stack    = True
    short_help    = 'Step instruction (possibly entering called functions)'

    def run(self, args):
        proc = self.proc
        core = self.core
        if len(args) <= 1:
            core.step_ignore = 0
        else:
            pos = 1
            if pos == len(args) - 1:
                core.step_ignore = proc.get_int(args[pos], default=1,
                                                          cmdname='step')
                if core.step_ignore is None: return False
                # 0 means stop now or step 1, so we subtract 1.
                core.step_ignore -= 1
                pass
            elif pos != len(args):
                self.errmsg("Invalid additional parameters %s"
                            % ' '.join(args[pos]))
                return False
            pass

        proc.vm.frame.event_flags = PyVMEVENT_ALL

        core.different_line   = True # Mcmdfns.want_different_line(args[0], self.settings['different'])
        core.stop_level       = None
        core.last_frame       = None
        core.stop_on_finish   = False
        proc.continue_running = True  # Break out of command read loop
        return True
    pass

if __name__ == '__main__':
    from trepan.processor.command.mock import MockDebugger
    d = MockDebugger()
    cmd = StepICommand(d.core.processor)
    for c in (['si', '5'],
              ['stepi', '1+2'],
              ['si', 'foo']):
        d.core.step_ignore = 0
        cmd.proc.continue_running = False
        result = cmd.run(c)
        print('Execute result: %s' % result)
        print('step_ignore %s' % repr(d.core.step_ignore))
        print('continue_running: %s' % cmd.proc.continue_running)
        pass
    # for c in (['si'], ['stepi']):
    #     d.core.step_ignore = 0
    #     cmd.continue_running = False
    #     result = cmd.run(c)
    #     print('different line %s:' % c[0], cmd.core.different_line)
    #     pass
    pass
