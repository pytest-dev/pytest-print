from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

EXAMPLE = "example3.py"


def extract_printer_text(lines: list[str], start_at: str) -> str:
    output = "\n".join(line for line in lines if not line.startswith("=" * 20))
    return output[output.find(start_at) :]


def fix_floats_in_relative_time(txt: str) -> str:
    float_pattern = r"[-+]?\d*\.\d+([eE][-+]?\d+)?"
    return re.sub(float_pattern, "0.1", txt)


def test_progress_v_no_relative(example: pytest.Testdir) -> None:
    result = example.runpytest("-v", "--print")
    result.assert_outcomes(passed=1)

    output = extract_printer_text(result.outlines, "test_example3.py::")
    spc, _tab = " ", "\t"
    assert (
        output
        == f"""
test_example3.py::test_pprinter_usage{spc}
  ⏩ start here the test start
      🚀 start a sub printer
          🧹 start a sub sub printer
          🔄 a message with a twist
          🧹 end a sub sub printer
      🚀 end a sub printer
  ⏩ end here the test end

test_example3.py::test_pprinter_usage PASSED                             [100%]
"""[1:]
    )


def test_progress_v_relative(example: pytest.Testdir) -> None:
    result = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
    )
    result.assert_outcomes(passed=1)

    output = extract_printer_text(result.outlines, "test_example3.py::")
    output = fix_floats_in_relative_time(output)

    spc, tab = " ", "\t"
    assert (
        output
        == f"""
test_example3.py::test_pprinter_usage{spc}
  ⏩ 0.1{tab}start here the test start
      🚀 0.1{tab}start a sub printer
          🧹 0.1{tab}start a sub sub printer
          🔄 0.1{tab}a message with a twist
          🧹 0.1{tab}end a sub sub printer
      🚀 0.1{tab}end a sub printer
  ⏩ 0.1{tab}end here the test end

test_example3.py::test_pprinter_usage PASSED                             [100%]
"""[1:]
    )
