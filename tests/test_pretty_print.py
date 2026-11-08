from __future__ import annotations

import re

import pytest

from ._helpers import extract_printer_text, seed_test


@pytest.fixture
def example(pytester: pytest.Pytester) -> pytest.Pytester:
    return seed_test("example_pretty_print.py", pytester)


def test_progress_v_no_relative(example: pytest.Pytester) -> None:
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


def test_progress_v_relative(example: pytest.Pytester) -> None:
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
    return re.sub(
        r"""
        [-+]?             # optional sign
        \d*\.\d+          # integer and fraction digits
        ([eE][-+]?\d+)?   # optional exponent
        """,
        "0.1",
        txt,
        flags=re.VERBOSE,
    )
