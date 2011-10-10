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

* See `test_includeh.h.meta <https://github.com/achauve/metapy/blob/master/tests/test_includeh.h.meta>`_ and the expected result `test_includeh.h <https://github.com/achauve/metapy/blob/master/tests/test_includeh.h.ref>`_.

* Generating the real files from the meta files can be easily integrated in your build environment. For example, with CMake, you can adapt the following macro::

    # macro to process meta files in a given source directory
    macro(meta src_dir) 
    file(GLOB_RECURSE meta_src ${src_dir}/*.meta)
        foreach(meta_file ${meta_src})
            string(REPLACE ".meta" "" file_to_generate ${meta_file})
            add_custom_command(OUTPUT ${file_to_generate}
                               COMMAND python ${WHERE_IS_LOCATED_METAPY}/metapy.py ${meta_file}
                               DEPENDS ${meta_file}
            )
            set(meta_gen ${meta_gen} ${file_to_generate})
        endforeach()
    endmacro()


Tests
=====

Run:

    python run_tests.py


License
=======

This code is released under the MIT License (see LICENSE.TXT for details).

Copyright © 2011 Adrien Chauve

