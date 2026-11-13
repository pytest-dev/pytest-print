from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

_FLOAT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""
    [-+]?             # optional sign
    \d*\.\d+          # integer and fraction digits
    ([eE][-+]?\d+)?   # optional exponent
    """,
    flags=re.VERBOSE,
)


@pytest.fixture
def example(seed_test: Callable[[str], pytest.Pytester]) -> pytest.Pytester:
    return seed_test("example_pretty_print.py")


def test_progress_v_no_relative(example: pytest.Pytester, extract_printer_text: Callable[[list[str]], str]) -> None:
    result = example.runpytest("-v", "--print")
    result.assert_outcomes(passed=1)

    output = extract_printer_text(result.outlines)
    expected = """\
test_a.py::test_pprinter_usage
   ⏩ start here the test start
      🚀 start an indented printer
         🧹 start an indented indented printer
         🔄 a message with a twist
         🧹 end an indented indented printer
      🚀 end an indented printer
   ⏩ end here the test end

test_a.py::test_pprinter_usage PASSED
"""
    assert output == expected


def test_progress_v_relative(example: pytest.Pytester, extract_printer_text: Callable[[list[str]], str]) -> None:
    result = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
    )
    result.assert_outcomes(passed=1)

    output = extract_printer_text(result.outlines)
    output = fix_floats_in_relative_time(output)

    expected = """\
test_a.py::test_pprinter_usage
  [0.1] ⏩ start here the test start
  [0.1]    🚀 start an indented printer
  [0.1]       🧹 start an indented indented printer
  [0.1]       🔄 a message with a twist
  [0.1]       🧹 end an indented indented printer
  [0.1]    🚀 end an indented printer
  [0.1] ⏩ end here the test end

test_a.py::test_pprinter_usage PASSED
"""
    assert output == expected


def fix_floats_in_relative_time(txt: str) -> str:
    return _FLOAT_PATTERN.sub("0.1", txt)
