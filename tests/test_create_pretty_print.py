from __future__ import annotations

import re

import pytest

from tests import extract_printer_text, seed_test


@pytest.fixture
def example(testdir: pytest.Testdir) -> pytest.Testdir:
    return seed_test("example_create_pretty_print.py", testdir)


def fix_floats_in_relative_time(txt: str) -> str:
    float_pattern = r"[-+]?\d*\.\d+([eE][-+]?\d+)?"
    return re.sub(float_pattern, "0.1", txt)


def test_progress_no_v(example: pytest.Testdir) -> None:
    result = example.runpytest()
    result.assert_outcomes(passed=3)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(example: pytest.Testdir) -> None:
    result_verbose = example.runpytest("-v", "--print")
    result_verbose.assert_outcomes(passed=3)

    output = extract_printer_text(result_verbose.outlines)

    expected = """\
test_a.py::test_global_peace
   ⏩ attempt global peace
   ⏩ here we have global peace

test_a.py::test_global_peace PASSED
test_a.py::test_server_parallel_requests
      🚀 create virtual environment
      🚀 start server from virtual env
      🚀 do the parallel request test

test_a.py::test_server_parallel_requests PASSED
test_a.py::test_create_pretty_printer_usage
.. ⏩ start here the test start
      🚀 start an indented printer
         🧹 start an indented indented printer
         🔄 a message with a twist
         🧹 end an indented indented printer
      🚀 end an indented printer
.. ⏩ end here the test end

test_a.py::test_create_pretty_printer_usage PASSED
   ⏩ teardown global peace
"""
    assert output == expected


def test_progress_v_relative(example: pytest.Testdir) -> None:
    result_verbose_relative = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
        "-k",
        "test_server_parallel_requests",
    )
    result_verbose_relative.assert_outcomes(passed=1)

    output = extract_printer_text(result_verbose_relative.outlines)
    output = fix_floats_in_relative_time(output)

    expected = """\
test_a.py::test_server_parallel_requests
  [0.1] ⏩ attempt global peace
  [0.1]    🚀 create virtual environment
  [0.1]    🚀 start server from virtual env
  [0.1]    🚀 do the parallel request test

test_a.py::test_server_parallel_requests PASSED
  [0.1] ⏩ teardown global peace
"""
    assert output == expected


def test_progress_no_v_but_with_print_request(example: pytest.Testdir) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=3)
    assert "      🚀 start server from virtual env" in result.outlines
    assert "   ⏩ attempt global peace" in result.outlines
