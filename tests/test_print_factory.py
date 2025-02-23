from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

EXAMPLE = "example2.py"


def extract_printer_text(lines: list[str], start_at: str) -> str:
    output = "\n".join(line for line in lines if not line.startswith("=" * 20))
    return output[output.find(start_at) :]


def fix_floats_in_relative_time(txt: str) -> str:
    float_pattern = r"[-+]?\d*\.\d+([eE][-+]?\d+)?"
    return re.sub(float_pattern, "0.1", txt)


def test_version() -> None:
    import pytest_print  # noqa: PLC0415

    assert pytest_print.__version__ is not None


def test_progress_no_v(example: pytest.Testdir) -> None:
    result = example.runpytest()
    result.assert_outcomes(passed=3)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(example: pytest.Testdir) -> None:
    result_verbose = example.runpytest("-v", "--print")
    result_verbose.assert_outcomes(passed=3)

    output = extract_printer_text(result_verbose.outlines, "test_example2.py::")

    spc, _tab = " ", "\t"
    assert (
        output
        == f"""
test_example2.py::test_global_peace{spc}
  ⏩ attempt global peace
  ⏩ here we have global peace

test_example2.py::test_global_peace PASSED                               [ 33%]
test_example2.py::test_server_parallel_requests{spc}
      🚀 create virtual environment
      🚀 start server from virtual env
      🚀 do the parallel request test

test_example2.py::test_server_parallel_requests PASSED                   [ 66%]
test_example2.py::test_pprinter_factory_usage{spc}
  ⏩ start here the test start
      🚀 start a sub printer
          🧹 start a sub sub printer
          🔄 a message with a twist
          🧹 end a sub sub printer
      🚀 end a sub printer
  ⏩ end here the test end

test_example2.py::test_pprinter_factory_usage PASSED                     [100%]
  ⏩ teardown global peace
"""[1:]
    )


def test_progress_v_relative(example: pytest.Testdir) -> None:
    result_verbose_relative = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
        "-k",
        "test_server_parallel_requests",
    )
    result_verbose_relative.assert_outcomes(passed=1)

    output = extract_printer_text(result_verbose_relative.outlines, "example2.py::test_server_parallel_requests")
    output = fix_floats_in_relative_time(output)

    spc, _tab = " ", "\t"
    assert (
        output
        == f"""
example2.py::test_server_parallel_requests{spc}
  ⏩ 0.1\tattempt global peace
      🚀 0.1\tcreate virtual environment
      🚀 0.1\tstart server from virtual env
      🚀 0.1\tdo the parallel request test

test_example2.py::test_server_parallel_requests PASSED                   [100%]
  ⏩ 0.1\tteardown global peace
"""[1:]
    )


def _test_progress_no_v_but_with_print_request(example: pytest.Testdir) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=3)
    assert "	start server from virtual env" in result.outlines
    assert "	attempt global peace" in result.outlines
