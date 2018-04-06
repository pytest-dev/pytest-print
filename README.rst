pytest-print
============

Allows to print extra content onto the PyTest reporting. This can be used for example to report sub-steps for long
running tests, or to print debug information in your tests when you cannot debug the code.

|pypi| |support| |licence|

|readthedocs| |travis| |appveyor| |coverage|

.. |pypi| image:: https://img.shields.io/pypi/v/pytest-print.svg?style=flat-square
    :target: https://pypi.org/project/pytest-print/
    :alt: pypi version

.. |support| image:: https://img.shields.io/pypi/pyversions/pytest-print.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pytest-print/
    :alt: supported Python version

.. |travis| image:: https://img.shields.io/travis/gaborbernat/pytest-print/master.svg?style=flat-square&label=Travis%20Build
    :target: https://travis-ci.org/gaborbernat/pytest-print
    :alt: travis build status

.. |appveyor| image:: https://img.shields.io/appveyor/ci/gaborbernat/pytest-print/master.svg?style=flat-square&logo=appveyor
    :target: https://ci.appveyor.com/project/gaborbernat/pytest-print
    :alt: appveyor build status

.. |coverage| image:: https://codecov.io/github/gaborbernat/pytest-print/coverage.svg?branch=master
    :target: https://codecov.io/github/gaborbernat/pytest-print?branch=master
    :alt: Code coverage

.. |licence| image:: https://img.shields.io/pypi/l/pytest-print.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pytest-print/
    :alt: licence

.. |readthedocs| image:: https://img.shields.io/readthedocs/pytest-print/latest.svg?style=flat-square&label=Read%20the%20Docs
   :alt: Read the documentation at https://pytest-print.readthedocs.io/en/latest/
   :target: https://pytest-print.readthedocs.io/en/latest/


install
=======

.. code-block:: sh

   pip install pytest-print

The plugin provides ability to print information during the tests runs.


use cases
=========

sub-step reporting
------------------
For tests that are long running this can provide a feedback ot the end-user that what is just happening in the
background.


.. code-block:: python

   def test_server_parallel_requests(pytest_print, tmpdir):
       pytest_print("create virtual environment into {}".format(tmpdir))
       create_virtual_environment(tmpdir)

       pytest_print("start server from virtual env")
       start_server(tmpdir)

       pytest_print("do the parallel request test")
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
