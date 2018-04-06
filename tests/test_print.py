# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def test_version():
    import pytest_print
    assert pytest_print.__version__


def test_printer_progress(testdir):
    testdir.makepyfile("""
def create_virtual_environment(tmpdir):
    pass

def start_server(tmpdir):
    pass

def parallel_requests():
    pass
        
def test_server_parallel_requests(printer, tmpdir):
       printer("create virtual environment")
       create_virtual_environment(tmpdir)

       printer("start server from virtual env")
       start_server(tmpdir)

       printer("do the parallel request test")
       parallel_requests()
    """)

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
    assert '	start server from virtual env' not in result.outlines

    result_verbose = testdir.runpytest('-v')
    result_verbose.assert_outcomes(passed=1)

    report_lines = ['test_printer_progress.py::test_server_parallel_requests ',
                    '\tcreate virtual environment',
                    '\tstart server from virtual env',
                    '\tdo the parallel request test']
    from_index = result_verbose.outlines.index(report_lines[0])
    assert result_verbose.outlines[from_index:from_index + len(report_lines)] == report_lines
