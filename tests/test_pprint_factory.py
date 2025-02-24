from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

EXAMPLE = "example2.py"


def extract_printer_text(lines: list[str], start_at: str) -> str:
    output = "\n".join(line for line in lines if not line.startswith("=" * 20))
    output = output[output.find(start_at) :]
    output = re.sub(r"\s*\[\s*\d+%\]", "", output)
    output = re.sub(f"test_{EXAMPLE}::", f"{EXAMPLE}::", output)
    return re.sub(r"[ \t]+\n", "\n", output)


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

    _spc, _tab = " ", "\t"
    assert (
        output
        == """
example2.py::test_global_peace
   ⏩ attempt global peace
   ⏩ here we have global peace

example2.py::test_global_peace PASSED
example2.py::test_server_parallel_requests
      🚀 create virtual environment
      🚀 start server from virtual env
      🚀 do the parallel request test

example2.py::test_server_parallel_requests PASSED
example2.py::test_pprinter_factory_usage
.. ⏩ start here the test start
      🚀 start a sub printer
         🧹 start a sub sub printer
         🔄 a message with a twist
         🧹 end a sub sub printer
      🚀 end a sub printer
.. ⏩ end here the test end

example2.py::test_pprinter_factory_usage PASSED
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

    output = extract_printer_text(result_verbose_relative.outlines, "test_example2.py::test_server_parallel_requests")
    output = fix_floats_in_relative_time(output)

    _spc, _tab = " ", "\t"
    assert (
        output
        == """
example2.py::test_server_parallel_requests
  [0.1] ⏩ attempt global peace
  [0.1]    🚀 create virtual environment
  [0.1]    🚀 start server from virtual env
  [0.1]    🚀 do the parallel request test

example2.py::test_server_parallel_requests PASSED
  [0.1] ⏩ teardown global peace
"""[1:]
    )


def test_progress_no_v_but_with_print_request(example: pytest.Testdir) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=3)
    assert "      🚀 start server from virtual env" in result.outlines
    assert "   ⏩ attempt global peace" in result.outlines
