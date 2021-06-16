from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.monkeypatch import MonkeyPatch
from _pytest.pytester import Testdir

_EXAMPLE = Path(__file__).parent / "example.py"


def test_version() -> None:
    import pytest_print

    assert pytest_print.__version__ is not None


@pytest.fixture()
def example(testdir: Testdir) -> Testdir:
    dest = Path(str(testdir.tmpdir / "test_example.py"))
    try:
        dest.symlink_to(_EXAMPLE)
    except OSError:  # pragma: no cover
        raise RuntimeError("requires symlink to test")  # pragma: no cover
    return testdir


def test_progress_no_v(example: Testdir) -> None:
    result = example.runpytest()
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" not in result.outlines
    assert "global peace" not in result.outlines


def test_progress_v_no_relative(example: Testdir, monkeypatch: MonkeyPatch) -> None:
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


def test_progress_v_relative(example: Testdir) -> None:
    result_verbose_relative = example.runpytest(
        "--print", "-v", "--print-relative-time", "-k", "test_server_parallel_requests"
    )
    out = "\n".join(result_verbose_relative.outlines)
    result_verbose_relative.assert_outcomes(passed=1)

    assert "example.py::test_server_parallel_requests " in out, out
    output = (i.split("\t") for i in result_verbose_relative.outlines if i.startswith("\t"))
    res = sorted((float(relative), msg) for _, relative, msg in output)

    assert [msg for _, msg in res] == [
        "attempt global peace",
        "create virtual environment",
        "start server from virtual env",
        "do the parallel request test",
        "teardown global peace",
    ], res


def test_progress_no_v_but_with_print_request(example: Testdir) -> None:
    result = example.runpytest("--print")
    result.assert_outcomes(passed=2)
    assert "	start server from virtual env" in result.outlines
    assert "	attempt global peace" in result.outlines
