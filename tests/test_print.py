from __future__ import annotations

import pytest

from tests import extract_printer_text, seed_test


@pytest.fixture
def example(pytester: pytest.Pytester) -> pytest.Pytester:
    return seed_test("example_print.py", pytester)


def test_progress_no_v(example: pytest.Pytester) -> None:
    result = example.runpytest()
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(example: pytest.Pytester, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("_pytest._io.terminalwriter.get_terminal_width", lambda: 80)
    monkeypatch.setenv("COLUMNS", str(80))
    result_verbose = example.runpytest("-v", "--print")
    result_verbose.assert_outcomes(passed=2)

    found = extract_printer_text(result_verbose.outlines)
    expected = """test_a.py::test_global_peace
	attempt global peace
	here we have global peace

test_a.py::test_global_peace PASSED
test_a.py::test_server_parallel_requests
	create virtual environment
	start server from virtual env
	do the parallel request test

test_a.py::test_server_parallel_requests PASSED
	teardown global peace
"""
    assert found == expected


def test_progress_v_relative(example: pytest.Pytester) -> None:
    result_verbose_relative = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
        "-k",
        "test_server_parallel_requests",
    )
    out = "\n".join(result_verbose_relative.outlines)
    result_verbose_relative.assert_outcomes(passed=1)

    assert "a.py::test_server_parallel_requests " in out, out
    output = (i.split("\t") for i in result_verbose_relative.outlines if i.startswith("\t"))
    found = [(float(relative), msg) for _, relative, msg in output]

    test = [m for _, m in sorted(i for i in found if "peace" not in i[1])]
    assert test == [
        "create virtual environment",
        "start server from virtual env",
        "do the parallel request test",
    ], test

    session = [m for _, m in sorted(i for i in found if "peace" in i[1])]
    assert session == [
        "attempt global peace",
        "teardown global peace",
    ], session


def test_progress_no_v_but_with_print_request(example: pytest.Pytester) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" in result.outlines
    assert "	attempt global peace" in result.outlines
