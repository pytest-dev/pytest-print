from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

EXAMPLE = "example3.py"


def extract_printer_text(lines: list[str], start_at: str) -> str:
    output = "\n".join(line for line in lines if not line.startswith("=" * 20))
    output = output[output.find(start_at) :]
    output = re.sub(r"\s*\[\s*\d+%\]", "", output)
    output = re.sub(f"test_{EXAMPLE}::", f"{EXAMPLE}::", output)
    return re.sub(r"[ \t]+\n", "\n", output)


def fix_floats_in_relative_time(txt: str) -> str:
    float_pattern = r"[-+]?\d*\.\d+([eE][-+]?\d+)?"
    return re.sub(float_pattern, "0.1", txt)


def test_progress_v_no_relative(example: pytest.Testdir) -> None:
    result = example.runpytest("-v", "--print")
    result.assert_outcomes(passed=1)

    output = extract_printer_text(result.outlines, "test_example3.py::")
    _spc, _tab = " ", "\t"
    assert (
        output
        == """
example3.py::test_pprinter_usage
   ⏩ start here the test start
      🚀 start a sub printer
         🧹 start a sub sub printer
         🔄 a message with a twist
         🧹 end a sub sub printer
      🚀 end a sub printer
   ⏩ end here the test end

example3.py::test_pprinter_usage PASSED
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

    _spc, _tab = " ", "\t"
    assert (
        output
        == """
example3.py::test_pprinter_usage
  [0.1] ⏩ start here the test start
  [0.1]    🚀 start a sub printer
  [0.1]       🧹 start a sub sub printer
  [0.1]       🔄 a message with a twist
  [0.1]       🧹 end a sub sub printer
  [0.1]    🚀 end a sub printer
  [0.1] ⏩ end here the test end

example3.py::test_pprinter_usage PASSED
"""[1:]
    )
