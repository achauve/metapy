===============
MetaPy
===============

MetaPy is a very simple python tool to generate code.


What does it do?
================

It finds the python code inside a text file, runs it, and replaces it by the
generated output.

This is well adapted for generating C++ code. For instance, if:

* you need variadic templates and cannot use c++11
* you need to adapt an API several times (use of external libraries,
  client/server API, ...)

you can use a few lines of simple python code instead of using very powerful
yet super-complex unreadable-two-days-after very-long-to-compile and
hard-to-debug-even-with-gcc--E boost::preprocessor-based macros! Insert python
code inside `/*# python code #*/` blocks, add a few prints and you're done.


Example
=======

See test_make_vector.cpp.meta and the expected result test_make_vector.cpp.ref.


Tests
=====

Run:

    python run_tests.py


License
=======

This code is released under the MIT License (see LICENSE.TXT for details).

Copyright © 2011 Adrien Chauve

