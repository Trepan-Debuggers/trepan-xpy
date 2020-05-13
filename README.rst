.. contents:: :local:

Abstract
========

This is a gdb-like debugger for `x-python <https://github.com/rocky/x-python>`_, the Python Interpeter written in Python.

Example
=======

::

   $ trepan-xpy test/example/gcd.py
   Running x-python test/example/gcd.py with ()
   (test/example/gcd.py:10): <module>
   -> 10 """
   (trepan-xpy) step
   (test/example/gcd.py:10): <module>
   -- 10 """
   L. 10  @  0: LOAD_CONST Greatest Common Divisor

   Some characterstics of this program used for testing:
   * check_args() does not have a 'return' statement.
   * check_args() raises an uncaught exception when given the wrong number
     of parameters.

   (trepan-xpy) set autopc
   Run `info pc` on debugger entry is on.
   (trepan-xpy) stepi
   (test/example/gcd.py:10 @2): <module>
   .. 10 """
          @  2: STORE_NAME __doc__
   PC offset is 2.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characterstics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
       -->     2 STORE_NAME          0          0

     11        4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

   (trepan-xpy) stepi
   (test/example/gcd.py:11 @4): <module>
   -- 11 import sys
   L. 11  @  4: LOAD_CONST 0
   PC offset is 4.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characterstics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     11-->     4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

   (trepan-xpy) info stack
   Evaluation stack is empty
   (trepan-xpy) stepi
   (test/example/gcd.py:11 @6): <module>
   .. 11 import sys
          @  6: LOAD_CONST None
   PC offset is 6.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characterstics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     11        4 LOAD_CONST          1          0
       -->     6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

   (trepan-xpy) info stack
    0: <class 'int'> 0
   (trepan-xpy) stepi
   (test/example/gcd.py:11 @8): <module>
   .. 11 import sys
          @  8: IMPORT_NAME sys
   PC offset is 8.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characterstics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     11        4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
       -->     8 IMPORT_NAME         1          1
              10 STORE_NAME          1          1

   (trepan-xpy) info stack
    0: <class 'NoneType'> None
    1: <class 'int'> 0
   (trepan-xpy) stepi
   (test/example/gcd.py:11 @10): <module>
   .. 11 import sys
          @ 10: STORE_NAME sys
   PC offset is 10.
     10        0 LOAD_CONST          0          "Greatest Common Divisor\n\nSome characterstics of this program used for testing: * check_args() does\nnot have a 'return' statement.\n\n* check_args() raises an uncaught exception when given the wrong number\n  of parameters.\n\n"
               2 STORE_NAME          0          0

     11        4 LOAD_CONST          1          0
               6 LOAD_CONST          2          None
               8 IMPORT_NAME         1          1
       -->    10 STORE_NAME          1          1

   (trepan-xpy) info stack
    0: <class 'module'> <module 'sys' (built-in)>
   (trepan-xpy) stepi
   (test/example/gcd.py:13 @12): <module>
   -- 13 def check_args():
   L. 13  @ 12: LOAD_CONST <code object check_args at 0x7fc7b90cea50, file "test/example/gcd.py", line 13>
   PC offset is 12.
     13-->    12 LOAD_CONST          3          <code object check_args at 0x7fc7b90cea50, file "test/example/gcd.py", line 13>
              14 LOAD_CONST          4          'check_args'
              16 MAKE_FUNCTION       0          No defaults, keyword-only args, annotations, or closures
              18 STORE_NAME          2          2

   (trepan-xpy) info stack
   Evaluation stack is empty
   (trepan-xpy) stepi
   (test/example/gcd.py:13 @14): <module>
   .. 13 def check_args():
          @ 14: LOAD_CONST check_args
   PC offset is 14.
     13       12 LOAD_CONST          3          <code object check_args at 0x7fc7b90cea50, file "test/example/gcd.py", line 13>
       -->    14 LOAD_CONST          4          'check_args'
              16 MAKE_FUNCTION       0          No defaults, keyword-only args, annotations, or closures
              18 STORE_NAME          2          2

   (trepan-xpy) stepi
   (test/example/gcd.py:13 @16): <module>
   .. 13 def check_args():
          @ 16: MAKE_FUNCTION annotation
   PC offset is 16.
     13       12 LOAD_CONST          3          <code object check_args at 0x7fc7b90cea50, file "test/example/gcd.py", line 13>
              14 LOAD_CONST          4          'check_args'
       -->    16 MAKE_FUNCTION       0          No defaults, keyword-only args, annotations, or closures
              18 STORE_NAME          2          2

   (trepan-xpy) info stack
    0: <class 'str'> 'check_args'
    1: <class 'code'> <code object ....py", line 13>
   (trepan-xpy) stepi
   (test/example/gcd.py:13 @18): <module>
   .. 13 def check_args():
          @ 18: STORE_NAME check_args
   PC offset is 18.
     13       12 LOAD_CONST          3          <code object check_args at 0x7fc7b90cea50, file "test/example/gcd.py", line 13>
              14 LOAD_CONST          4          'check_args'
              16 MAKE_FUNCTION       0          No defaults, keyword-only args, annotations, or closures
       -->    18 STORE_NAME          2          2

   (trepan-xpy) info stack
    0: <class 'function'> <function che...x7fc7b906f7a0>
   (trepan-xpy) continue
     File "test/example/gcd.py", line 41, in <module>
       check_args()
     File "test/example/gcd.py", line 16, in check_args
       raise Exception("Need to give two numbers")
   Exception: Need to give two numbers
   (test/example/gcd.py:16 @20): check_args
   XX 16         raise Exception("Need to give two numbers")
   PC offset is 20.
     16       14 LOAD_GLOBAL         3          3
              16 LOAD_CONST          2          'Need to give two numbers'
              18 CALL_FUNCTION       1          1 positional argument
       -->    20 RAISE_VARARGS       1

     17   >>  22 SETUP_LOOP          102        to 126
              24 LOAD_GLOBAL         4          4
              26 LOAD_CONST          3          2
              28 CALL_FUNCTION       1          1 positional argument
              30 GET_ITER            None
   (trepan-xpy:pm) list
    17    	    for i in range(2):
    18    	        try:
    19    	            sys.argv[i+1] = int(sys.argv[i+1])
    20    	        except ValueError:
    21    	            print("** Expecting an integer, got: %s" % repr(sys.argv[i]))
    22    	            sys.exit(2)
    23    	            pass
    24    	        pass
    25
    26    	def gcd(a,b):
   (trepan-xpy:pm) Leaving
   trepan-xpy: That's all, folks...


See Also
--------

* trepan3_ : trepan debugger for Python 3.x

.. _trepan3: https://github.com/rocky/python3-trepan
