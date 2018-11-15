pytest-print
============

Allows to print extra content onto the PyTest reporting. This can be used for example to report sub-steps for long
running tests, or to print debug information in your tests when you cannot debug the code.

.. image:: https://badge.fury.io/py/pytest_print.svg
  :target: https://badge.fury.io/py/pytest_print
  :alt: Latest version on PyPI
.. image:: https://img.shields.io/pypi/pyversions/pytest_print.svg
  :target: https://pypi.org/project/pytest_print/
  :alt: Supported Python versions
.. image:: https://dev.azure.com/pytestdev/pytest_print/_apis/build/status/pytest_print%20ci?branchName=master
  :target: https://dev.azure.com/pytestdev/pytest_print/_build/latest?definitionId=9&branchName=master
  :alt: Azure Pipelines build status
.. image:: https://api.codeclimate.com/v1/badges/425c19ab2169a35e1c16/test_coverage
   :target: https://codeclimate.com/github/pytest_print-dev/pytest_print/code?sort=test_coverage
   :alt: Test Coverage
.. image:: https://readthedocs.org/projects/pytest_print/badge/?version=latest&style=flat-square
  :target: https://pytest_print.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation status
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/ambv/black
  :alt: Code style: black


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
