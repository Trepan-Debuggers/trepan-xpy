.. contents:: :local:

Abstract
========

This is a gdb-like debugger focusing on Python bytecode. So far as I know, this is the *only* debugger available specifically for Python bytecode.

However to do this, you need to use underneath `x-python <https://pypi.org/project/x-python>`_: a Python Interpreter written in Python.

This project builds off of a previous Python 3 debugger called `trepan3k <https://pypi.org/project/trepan3k/>`_.


Example
=======

|demo|

We'll invoke the a Greatest Common Divisors program (`gcd.py`) using our debugger. The source is found in `test/example/gcd.py <https://github.com/rocky/trepan-xpy/blob/master/test/example/gcd.py>`_.

In this section we'll these some interesting debugger commands that are not common in Python debuggers:

* ``stepi`` to step a bytecode instruction
* ``set autopc`` to show a disassembly around the current program counter (PC)
* ``info stack`` to show the current stack frame evaluation stack

.. raw:: html

   <pre>$ <b>trepan-xpy test/example/gcd.py</b>
    Running x-python test/example/gcd.py with ()
    (test/example/gcd.py:10): &lt;module&gt;
    -&gt; 10 &quot;&quot;&quot;
    (trepan-xpy)
    </pre>
    $ trepan-xpy test/example/gcd.py
       Running x-python test/example/gcd.py with ()
       (test/example/gcd.py:10): <module>
       -> 10 """
    </pre>

Above we are stopped before we have even run the first instruction. The ``->`` icon before ``10`` means we are stopped calling a new frame.

.. raw:: html

    <pre>(trepan-xpy) <b>step</b>
    (test/example/gcd.py:10): &lt;module&gt;
    -- 10 <font color="#C4A000">&quot;&quot;&quot;</font>
           @  0: <font color="#4E9A06">LOAD_CONST</font> <font color="#C4A000">&quot;Greatest Common Divisor\n\nSome characterstics of this program used for testing:\n\n* check_args() does not have a &apos;return&apos; statement.\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n&quot;</font>
    </pre>

Ok, now we are stopped before the first instruction `LOAD_CONST` which will load a constant onto the evaluation stack.
The icon changed from ``-> 10`` to ``-- 10`` which indicates we are on a line number boundary at line 10.

The Python construct we are about to perform is setting the program's docstring. Let's see how that is implemented.
We see here that the first part is loading this constant onto an evaluation stack.

To better see the execution progress we'll issue the command `set autopc` which will show the instructions as we step along.

.. raw:: html

    <pre>(trepan-xpy) <b>set autopc</b>
    <i>Run `info pc` on debugger entry is on.</i>
    (trepan-xpy)</pre>
    </pre>

A rather unique command that you won't find in most Python debuggers but is in low-level debuggers is ``stepi`` which steps
and instruction. Let's use that:

.. raw:: html

    <pre>(trepan-xpy) <b>stepi</b>
    (test/example/gcd.py:10 @2): <module>
    .. 10 &quot;&quot;&quot;
             @  2: STORE_NAME <i>__doc__</i>
    PC offset is 2.
       10        0 LOAD_CONST          0          <i>"Greatest Common Divisor\n\nSome characterstics of this program used for testing:\n\n* check_args() does not have a 'return' statement.\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"</i>
         <b>--&gt;</b>     2 STORE_NAME          0          <i>__doc__</i>

       11        4 LOAD_CONST          1          0
                 6 LOAD_CONST          2          <i>None</i>
                 8 IMPORT_NAME         1          <i>sys</i>
                10 STORE_NAME          1          <i>sys</i>
    </pre>


The ``..`` at the beginning indicate that we are on an instruction which is in between lines.
We've now loaded the docstring onto the evaluation stack with ``LOAD_CONST`` Let's see the evaluation stack with ``info stack``

.. raw:: html

   <pre>(trepan-xpy) <b>info stack</b>
   0: <class 'str'> <i>'Greatest Com...rameters.\n\n'</i>
   </pre>

Here we have pushed the docstring for the program but haven't yet stored that in ``__doc__`` to see this we'll use ``info locals`` to see the local variables:

::

   (trepan-xpy) info locals

   __builtins__ = <module 'builtins' (built-in)>
   __doc__ = file
   __None__ = 'test/example/gcd.py'
   __loader__ = None
   __name__ = '__main__'
   __package__ = None
   __spec__ = None

Let's step the remaining instruction, ``STORE_NAME`` to complete the instructions making up line 1.

.. raw:: html

   <pre>(trepan-xpy) <b>stepi</b>
   (test/example/gcd.py:11 @4): <module>
   -- 11 import sys
   L. 11  @  4: LOAD_CONST 0
   PC offset is 4.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characteristics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     <b>11--&gt;</b>     4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1
   </pre>

The ``--`` at the beginning indicates we are on a line boundary now. Let's see the stack now that we have run ``STORE_NAME``:

.. raw:: html

   <pre>(trepan-xpy) <b>info stack</b>
   <i>Evaluation stack is empty</i>
   </pre>


And to see that we've stored this in ``__doc__`` we can run ``eval`` to see its value:

.. raw:: html

    <pre>(trepan-xpy) <b>eval __doc__</b>
    "Greatest Common Divisor\n\nSome characteristics of this program used for testing:\n\n* check_args() does not have a 'return' statement.\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
    </pre>


I invite you to continue stepping this program to see

* how functions get created
* how functions are called
* what happens when an exception is raised

and much more.

Here are some interesting commands not typically found in Python debuggers, like ``pdb``

* ``info blocks`` lets you see the block stack
* ``set pc <offset>`` lets you set the Program counter within the frame
* ``return <value>`` lets you cause an immediate return with a value
* ``shell`` go into a python interactive shell *with access to the current frame and Virtual Machine*


See Also
=========

* xpython_ : CPython written in Python
* trepan3k_ : trepan debugger for Python 3.x and its extensive documentation_.

.. _xpython: https://pypi.org/project/x-python/
.. _trepan3k: https://pypi.org/project/trepan3k/
.. _documentation: https://python3-trepan.readthedocs.io/en/latest/

.. |demo| image:: https://github.com/rocky/trepan-xpy/blob/master/screenshots/trepan-xpy-demo1.gif
