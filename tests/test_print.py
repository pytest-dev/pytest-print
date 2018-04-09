# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest


def test_version():
    import pytest_print
    assert pytest_print.__version__


@pytest.fixture(name='progress_report_example')
def progress_report_example_fixture(testdir):
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
    yield testdir


def test_progress_no_v(progress_report_example):
    result = progress_report_example.runpytest()
    result.assert_outcomes(passed=1)
    assert '	start server from virtual env' not in result.outlines


def test_progress_v_no_relative(progress_report_example):
    result_verbose = progress_report_example.runpytest('-v')
    result_verbose.assert_outcomes(passed=1)

    report_lines = ['test_progress_v_no_relative.py::test_server_parallel_requests ',
                    '\tcreate virtual environment',
                    '\tstart server from virtual env',
                    '\tdo the parallel request test']
    from_index = result_verbose.outlines.index(report_lines[0])
    assert result_verbose.outlines[from_index:from_index + len(report_lines)] == report_lines


def test_progress_v_relative(progress_report_example):
    result_verbose_relative = progress_report_example.runpytest('-v', '--print-relative-time')
    result_verbose_relative.assert_outcomes(passed=1)

    from_index = result_verbose_relative.outlines.index('test_progress_v_relative.py::test_server_parallel_requests ')
    output = (i.split('\t') for i in
              result_verbose_relative.outlines[from_index + 1:from_index + 4])
    out = sorted([(float(relative), msg) for _, relative, msg in output])

    assert [msg for _, msg in out] == ['create virtual environment',
                                       'start server from virtual env',
                                       'do the parallel request test']
