from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

_EXAMPLE = Path(__file__).parent / "example.py"


def test_version() -> None:
    import pytest_print  # noqa: PLC0415

    assert pytest_print.__version__ is not None


@pytest.fixture
def example(testdir: pytest.Testdir) -> pytest.Testdir:
    dest = Path(str(testdir.tmpdir)) / "test_example.py"
    copy2(str(_EXAMPLE), str(dest))
    return testdir


def test_progress_no_v(example: pytest.Testdir) -> None:
    result = example.runpytest()
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(example: pytest.Testdir, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("_pytest._io.terminalwriter.get_terminal_width", lambda: 80)
    monkeypatch.setenv("COLUMNS", str(80))
    result_verbose = example.runpytest("-v", "--print")
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
    found = result_verbose.outlines[from_index : from_index + len(report_lines)]
    assert found == report_lines


def test_progress_v_relative(example: pytest.Testdir) -> None:
    result_verbose_relative = example.runpytest(
        "--print",
        "-v",
        "--print-relative-time",
        "-k",
        "test_server_parallel_requests",
    )
    out = "\n".join(result_verbose_relative.outlines)
    result_verbose_relative.assert_outcomes(passed=1)

    assert "example.py::test_server_parallel_requests " in out, out
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


def test_progress_no_v_but_with_print_request(example: pytest.Testdir) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" in result.outlines
    assert "	attempt global peace" in result.outlines
