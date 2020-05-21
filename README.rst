.. contents:: :local:

Abstract
========

This is a gdb-like debugger for `x-python <https://github.com/rocky/x-python>`_, the Python Interpreter written in Python.

Example
=======

We'll invoke the a Greatest Common Divisors program (`gcd.py`) using our debugger. The source is found in `test/example/gcd.py <https://github.com/rocky/trepan-xpy/blob/master/test/example/gcd.py>`_.

In this section we'll these some interesting debugger commands that are not common in Python debuggers:

* ``stepi`` to step a bytecode instruction
* ``set autopc`` to show a disassembly around the current program counter (PC)
* ``info stack`` to show the current stack frame evaluation stack

::

   $ trepan-xpy test/example/gcd.py
   Running x-python test/example/gcd.py with ()
   (test/example/gcd.py:10): <module>
   -> 10 """

Above we are stopped before we have even run the first instruction. The ``->`` icon before ``10`` means we are stopped calling a new frame.

::

   (trepan-xpy) step
   (test/example/gcd.py:10): <module>
   -- 10 """
   L. 10  @  0: LOAD_CONST Greatest Common Divisor

   Some characteristics of this program used for testing:
   * check_args() does not have a 'return' statement.
   * check_args() raises an uncaught exception when given the wrong number
     of parameters.

Ok, now we are stopped before the first instruction `LOAD_CONST` which will load a constant onto the evaluation stack.
The icon changed from ``-> 10`` to ``-- 10`` which indicates we are on a line number boundary at line 10.

The Python construct we are about to perform is setting the program's docstring. Let's see how that is implemented.
We see here that the first part is loading this constant onto an evaluation stack.

To better see the execution progress we'll issue the command `set autopc` which will show the instructions as we step along.

::

   (trepan-xpy) set autopc
   Run `info pc` on debugger entry is on.

A rather unique command that you won't find in most Python debuggers but is in low-level debuggers is ``stepi`` which steps
and instruction. Let's use that:

::

   (trepan-xpy) stepi
   (test/example/gcd.py:10 @2): <module>
   .. 10 """
           @  2: STORE_NAME __doc__
   PC offset is 2.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characteristics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
       -->     2 STORE_NAME          0          0

     11        4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

The ``..`` at the beginning indicate that we are on an instruction which is in between lines.
We've now loaded the docstring onto the evaluation stack with ``LOAD_CONST`` Let's see the evaluation stack with ``info stack``

::

   (trepan-xpy) info stack
   0: <class 'str'> 'Greatest Com...rameters.\n\n'

Here we have pushed the docstring for the program but haven't yet stored that in ``__doc__`` to see this we'll use ``info locals`` to see the local variables:

::

   (trepan-xpy) info locals

   __builtins__ = <module 'builtins' (built-in)>
   __doc__ = None
   __file__ = 'test/example/gcd.py'
   __loader__ = None
   __name__ = '__main__'
   __package__ = None
   __spec__ = None

Let's step the remaining instruction, `STORE_NAME` to complete the instructions making up line 1.

::

   (trepan-xpy) stepi
   (test/example/gcd.py:11 @4): <module>
   -- 11 import sys
   L. 11  @  4: LOAD_CONST 0
   PC offset is 4.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characteristics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     11-->     4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

The ``--`` at the beginning indicates we are on a line boundary now. Let's see the stack now that we have run `S`TORE_NAME``:

::

   (trepan-xpy) info stack
   Evaluation stack is empty


And to see that we've stored this in ``__doc__`` we can run `eval` to see its value:

::

    (trepan-xpy) eval __doc__
    "Greatest Common Divisor\n\nSome characteristics of this program used for testing:\n\n* check_args() does not have a 'return' statement.\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"


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

* trepan3_ : trepan debugger for Python 3.x and its extensive documentation_.

.. _trepan3: https://github.com/rocky/python3-trepan
.. _documentation: https://python3-trepan.readthedocs.io/en/latest/
