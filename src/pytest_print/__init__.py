"""Pytest print functionality."""

from __future__ import annotations

from timeit import default_timer
from typing import TYPE_CHECKING, Callable

import pytest

from ._version import __version__

if TYPE_CHECKING:
    from _pytest.config.argparsing import Parser
    from _pytest.fixtures import SubRequest
    from _pytest.terminal import TerminalReporter


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--print-relative-time",
        action="store_true",
        dest="pytest_print_relative_time",
        default=False,
        help="Time in milliseconds when the print was invoked, relative to the time the fixture was created.",
    )
    group.addoption(
        "--print",
        action="store_true",
        dest="pytest_print_on",
        default=False,
        help="By default the plugins if verbosity is greater than zero (-v flag), this forces on",
    )


@pytest.fixture(name="printer")
def printer(request: SubRequest) -> Callable[[str], None]:
    """Pytest plugin to print test progress steps in verbose mode."""
    return create_printer(request)


@pytest.fixture(scope="session", name="printer_session")
def printer_session(request: SubRequest) -> Callable[[str], None]:
    return create_printer(request)


def create_printer(request: SubRequest) -> Callable[[str], None]:
    if request.config.getoption("pytest_print_on") or request.config.getoption("verbose") > 0:
        terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
        if terminal_reporter is not None:  # pragma: no branch
            state = State(request.config.getoption("pytest_print_relative_time"), terminal_reporter)
            return state.printer

    return no_op


def no_op(msg: str) -> None:
    """Do nothing."""


class State:
    def __init__(self, print_relative: bool, reporter: TerminalReporter) -> None:  # noqa: FBT001
        self._reporter = reporter
        self._start = default_timer() if print_relative else None
        self._print_relative = print_relative

    @property
    def elapsed(self) -> float | None:
        if self._start is None:
            return None  # pragma: no cover
        return default_timer() - self._start

    def printer(self, msg: str) -> None:
        msg = "\t{}{}".format(f"{self.elapsed}\t" if self._print_relative else "", msg)
        self._reporter.write_line(msg)

    __slots__ = ("_print_relative", "_reporter", "_start")


__all__ = [
    "__version__",
]
