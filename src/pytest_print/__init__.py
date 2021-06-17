from datetime import datetime
from typing import Callable, Optional

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.terminal import TerminalReporter

from .version import __version__


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
    """pytest plugin to print test progress steps in verbose mode"""
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


def no_op(msg: str) -> None:  # noqa: U100
    """Do nothing"""


class State:
    def __init__(self, print_relative: bool, reporter: TerminalReporter) -> None:
        self._reporter = reporter
        self._start = datetime.now() if print_relative else None
        self._print_relative = print_relative

    @property
    def elapsed(self) -> Optional[float]:
        if self._start is None:
            return None  # pragma: no cover
        return (datetime.now() - self._start).total_seconds()

    def printer(self, msg: str) -> None:
        msg = "\t{}{}".format(f"{self.elapsed}\t" if self._print_relative else "", msg)
        self._reporter.write_line(msg)

    __slots__ = ("_start", "_print_relative", "_reporter")


__all__ = [
    "__version__",
]
