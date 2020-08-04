# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from shutil import copy2

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))


def test_version():
    import pytest_print

    assert pytest_print.__version__


@pytest.fixture(name="progress_report_example")
def progress_report_example_fixture(testdir):
    copy2(os.path.join(HERE, "example.py"), str(testdir.tmpdir / "test_example.py"))
    yield testdir


def test_progress_no_v(progress_report_example):
    result = progress_report_example.runpytest()
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(progress_report_example):
    result_verbose = progress_report_example.runpytest("-v", "--print")
    result_verbose.assert_outcomes(passed=2)

    report_lines = [
        "test_example.py::test_global_peace ",
        "\tattempt global peace",
        "\there we have global peace",
        "",
        "test_example.py::test_global_peace PASSED                                [ 50%]",
        "test_example.py::test_server_parallel_requests ",
        "\tcreate virtual environment",
        "\tstart server from virtual env",
        "\tdo the parallel request test",
        "",
        "test_example.py::test_server_parallel_requests PASSED                    [100%]",
        "\tteardown global peace",
    ]
    from_index = result_verbose.outlines.index(report_lines[0])
    assert result_verbose.outlines[from_index : from_index + len(report_lines)] == report_lines


def test_progress_v_relative(progress_report_example):
    result_verbose_relative = progress_report_example.runpytest("--print", "-v", "--print-relative-time")
    out = "\n".join(result_verbose_relative.outlines)
    result_verbose_relative.assert_outcomes(passed=2)

    marker = "test_example.py::test_global_peace "
    assert marker in result_verbose_relative.outlines, out
    output = (i.split("\t") for i in result_verbose_relative.outlines if i.startswith("\t"))
    out = sorted([(float(relative), msg) for _, relative, msg in output])

    assert [msg for _, msg in out] == [
        "attempt global peace",
        "here we have global peace",
        "create virtual environment",
        "start server from virtual env",
        "do the parallel request test",
        "teardown global peace",
    ], out


def test_progress_no_v_but_with_print_request(progress_report_example):
    result = progress_report_example.runpytest("--print")
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" in result.outlines
    assert "	attempt global peace" in result.outlines
