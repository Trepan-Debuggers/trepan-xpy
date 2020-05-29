.. contents:: :local:

Abstract
========

This is a gdb-like debugger focusing on Python bytecode. So far as I know, this is the *only* debugger available specifically for Python bytecode.

However to do this, you need to use underneath `x-python <https://pypi.org/project/x-python>`_: a Python Interpreter written in Python.

This project builds off of a previous Python 3 debugger called `trepan3k <https://pypi.org/project/trepan3k/>`_.


Example
=======

|demo|

Below we'll try to break down what's going on above.

We'll invoke the a Greatest Common Divisors program (`gcd.py`) using our debugger. The source is found in `test/example/gcd.py <https://github.com/rocky/trepan-xpy/blob/master/test/example/gcd.py>`_.

In this section we'll these some interesting debugger commands that are not common in Python debuggers:

* ``stepi`` to step a bytecode instruction
* ``set logtrace`` to show a the x-python log "info"-level log tracing.
* ``info stack`` to show the current stack frame evaluation stack

.. raw:: html

   <pre>$ <b>trepan-xpy test/example/gcd.py 3 5</b>
    Running x-python test/example/gcd.py with ('3', '5')
    (test/example/gcd.py:10): &lt;module&gt;
    -&gt; 2 &quot;&quot;&quot;
    (trepan-xpy)
    </pre>

Above we are stopped before we have even run the first instruction. The ``->`` icon before ``2`` means we are stopped calling a new frame.

.. raw:: html

    <pre>(trepan-xpy) <b>step</b>
    (test/example/gcd.py:2): &lt;module&gt;
    -- 2 <font color="#C4A000">&quot;&quot;&quot;Greatest Common Divisor&quot;&quot;&quot;</font>
           @  0: <font color="#4E9A06">LOAD_CONST</font> <font color="#C4A000">&apos;Greatest Common Divisor&apos;</font>
    </pre>

Ok, now we are stopped before the first instruction ``LOAD_CONST`` which will load a constant onto the evaluation stack.
The icon changed from ``-> 2`` to ``-- 2`` which indicates we are on a line-number boundary at line 2.

The Python construct we are about to perform is setting the program's docstring. Let's see how that is implemented.

First we see that the variable ``__doc__`` which will eventually hold the docstring isn't set:

We see here that the first part is loading this constant onto an evaluation stack.

.. raw:: html
    </pre>(trepan-xpy) __doc__
    </pre>


At this point, to better see the execution progress we'll issue the command `set logtrace` which will show the instructions as we step along.

Like *trepan3k*, *trepan-xpy* has extensive nicely formatted help right in the debugger. Let's get the help for the ``set logtrace`` command:

.. raw:: html

    <pre>(trepan-xpy) <b>help set logtrace</b>
    <b>set logtrace</b> [ <b>on</b> | <b>off</b> | <b>debug</b> | <b>info</b> ]

    Show logtrace PyVM logger messages. Initially logtracing is off.

    However running set logtrace will turn it on and set the log level to debug.
    So it's the same thing as set logtrace debug.

    If you want the less verbose messages, use info. And to turn off, (except
    critical errors), use off.

    Examples:

         set logtrace         # turns x-python on info logging messages
         set logtrace info    # same as above
         set logtrace debug   # turn on info and debug logging messages
         set logtrace off     # turn off all logging messages except critical ones


    </pre>

So now lets's set that
.. raw:: html

    <pre>(trepan-xpy) <b>set logtrace</b>
    <pre>(trepan-xpy)

A rather unique command that you won't find in most Python debuggers but is in low-level debuggers is ``stepi`` which steps and instruction. Let's use that:

.. raw:: html
    <pre><pre>(trepan-xpy) <b>stepi</b>
    (test/example/gcd.py:2 @2): &lt;module&gt;
    .. 2 &quot;&quot;&quot;Greatest Common Divisor&quot;&quot;&quot;
           @  2: STORE_NAME &apos;Greatest Common Divisor&apos;) <i>__doc__</i>
    </pre>

The ``..`` at the beginning indicates that we are on an instruction which is in between lines.

We've now loaded the docstring onto the evaluation stack with ``LOAD_CONST`` Let's see the evaluation stack with ``info stack``

.. raw:: html

   <pre>(trepan-xpy) <b>info stack</b>
     0: &lt;class &apos;str&apos;&gt; &apos;Greatest Common Divisor&apos;
   </pre>

Here we have pushed the docstring for the program but haven't yet stored that in ``__doc__`` to see this can use the fact that `trepan-xpy` will automatically evaluate strings it doesn't recognize as a debugger command:

.. raw:: html

   <pre>(trepan-xpy) <b>__doc__ is None</b>
   True
   </pre>

Let's step the remaining instruction, ``STORE_NAME`` to complete the instructions making up line 1.

.. raw:: html

    <pre>trepan-xpy) <b>stepi</b>
    INFO:xpython.vm:L. 10  @  4: LOAD_CONST 0
    (test/example/gcd.py:10 @4): &lt;module&gt;
    -- 10 import <u>sys</u>
       @  4: LOAD_CONST 0
    </pre>

The ``--`` before ``10 import...` at the beginning indicates we are on a line boundary now. Let's see the stack now that we have run ``STORE_NAME``:

.. raw:: html

   <pre>(trepan-xpy) <b>info stack</b>
   <i>Evaluation stack is empty</i>
   </pre>


And to see that we've stored this in ``__doc__`` we can run ``eval`` to see its value:

.. raw:: html

    <pre>(trepan-xpy) <b>eval __doc__</b>
    "Greatest Common Divisor"
    </pre>


Now let's step a statement (not instructions), to see how a module becomes visable.

.. raw:: html

    <pre>(trepan-xpy) <b>step</b>
    INFO:xpython.vm:       @  6: LOAD_CONST None
    INFO:xpython.vm:       @  8: IMPORT_NAME (0, None) <i>sys</i>
    INFO:xpython.vm:       @ 10: STORE_NAME (&lt;module &apos;sys&apos; (built-in)&gt;)
    INFO:xpython.vm:L. 12  @ 12: LOAD_CONST &lt;code object check_args at 0x7f2a0a286f60, file &quot;test/example/gcd.py&quot;, line 12&gt;
    (test/example/gcd.py:12 @12): &lt;module&gt;
    -- 12 <b>def</b> check_args</font>():
       @ 12: LOAD_CONST &lt;code object check_args at 0...est/example/gcd.py&quot;, line 12&gt;
    </pre>

The ```INFO`` lines come from the VM interpreter, as a result of the ``set logtrace`` a callback is made to a formatting function provided by the debugger was called to print the information, and that is why parts of this are colorized in a terminal session. However since we were not statement stepping, the debugger's event loop and REPL was not involved running the statement.

One thingof node are the value after the operatnd and in parenthesis, like after ``STORE NAME``. Cmpare that line with what you'll see from a static disassembly like Python's ``dis`` or ``xdis`` version of that:

::
    10 STORE_NAME                1 (sys)

In a static disassembler, the "1" indicates the name index in the code object. The value in parenthesis is what that name, here at index 1 is, namely `sys`.

In ``trepan-xpy`` and ``x-python`` however we omit the name index, 1, since that isn't of much interest. Instead we show that dynamic stack entries or operands that ``STORE_NAME`` is going to work on. In particular the object that is going to be stored in variable ``sys`` is the built-in module ``sys``.

Now let's step another statement to see how a function becomes available:

.. raw:: html

    <pre>trepan-xpy) step
    INFO:xpython.vm:       @ 14: LOAD_CONST &apos;check_args&apos;</font>
    INFO:xpython.vm:       @ 16: MAKE_FUNCTION (check_args) Neither defaults, keyword-only args, annotations, nor closures
    INFO:xpython.vm:       @ 18: STORE_NAME (&lt;Function check_args at 0x7fdb1d4d49f0&gt;) <u>check_args</u>
    INFO:xpython.vm:L. 25  @ 20: LOAD_CONST &lt;code object gcd at 0x7fdb1d55fed0, file &quot;test/example/gcd.py&quot;, line 25&gt;
    (test/example/gcd.py:25 @20): &lt;module&gt;
    -- 25 <b>def</b> gcd(a,b):
           @ 20: LOAD_CONST &lt;code object gcd at 0x7fdb1d...est/example/gcd.py&quot;, line 25&gt;
    </pre>

A different between a dynamic language like Python and a statically compiled language like C, or Java is that there is no linking step in the complation, modules and functions are imported and linked as part of the execution of the code.

Notice again what's in the parenthesis after the opcode and how that differens from a static disassembly. For comparison here is what 2nd and 3rd instruction look like from pydisasm:

```
              16 MAKE_FUNCTION             0 (Neither defaults, keyword-only args, annotations, nor closures)
              18 STORE_NAME                2 (check_args)
```

Again indices into a name table are dropped and in their place are the evaluation stack items. For ``MAKE_FUNCTION` the name of the function that is created is shown; while for ``STORE_NAME`` again the item that gets stored (a function object) is shown.

The rest of the video shows, we show that in addition to ``step`` (step into) and ``stepi`` (step instruction) debugger commands there is a ``next`` or step over debugger command.
Also in contrast to any other Python debugger I know about, we can cause an immediate return with a value.

We've only show a few of the many debugger features.

Here are some interesting commands not typically found in Python debuggers, like ``pdb``

* ``info blocks`` lets you see the block stack
* ``set pc <offset>`` lets you set the Program counter within the frame
* ``set autopc>`` run ``info pc`` to get the debugged program's program counter every time bofore the debugger its ERPL


See Also
=========

* xpython_ : CPython written in Python
* trepan3k_ : trepan debugger for Python 3.x and its extensive documentation_.

.. _xpython: https://pypi.org/project/x-python/
.. _trepan3k: https://pypi.org/project/trepan3k/
.. _documentation: https://python3-trepan.readthedocs.io/en/latest/

.. |demo| image:: https://github.com/rocky/trepan-xpy/blob/master/screenshots/trepan-xpy-demo1.gif
