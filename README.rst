pytest-print
============

Allows to print extra content onto the PyTest reporting. This can be used for example to report sub-steps for long
running tests, or to print debug information in your tests when you cannot debug the code.

install
=======

.. code-block:: sh

   pip install pytest-print

The plugin provides ability to print information during the tests runs.

flags
=====
* ``--print`` by default the module activates print when pytest verbosity is greater than zero, this allows to bypass
  this and force print irrespective of the verbosity
* ``--print-relative-time`` will print the relative time since the start of the test (display how long it takes to reach
  prints)

use cases
=========

sub-step reporting
------------------
For tests that are long running this can provide a feedback ot the end-user that what is just happening in the
background.


.. code-block:: python

   def test_server_parallel_requests(printer, tmpdir):
       printer("create virtual environment into {}".format(tmpdir))
       create_virtual_environment(tmpdir)

       printer("start server from virtual env")
       start_server(tmpdir)

       printer("do the parallel request test")
       parallel_requests()

.. code-block:: sh

    $ py.test --vv
    ============================= test session starts ==============================
    platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
    collecting ... collected 1 item

    test_printer_progress.py::test_server_parallel_requests
        create virtual environment
        start server from virtual env
        do the parallel request test
    PASSED                                                                   [100%]

    =========================== 1 passed in 0.02 seconds ===========================
