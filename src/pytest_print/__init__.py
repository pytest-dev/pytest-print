"""Pytest print functionality."""

from __future__ import annotations

import dataclasses as dc
from timeit import default_timer
from typing import TYPE_CHECKING, Callable, Protocol

import pytest

from ._version import __version__

if TYPE_CHECKING:
    from _pytest.capture import CaptureManager
    from _pytest.config.argparsing import Parser
    from _pytest.fixtures import SubRequest
    from _pytest.terminal import TerminalReporter


# define some datatypes for the pprint and pprinter_factory fixtures


class PPrinterType(Protocol):
    def subprinter(self, icon: str | None = None) -> PPrinterType: ...

    def __call__(self, msg: str, icon: str | None = None) -> None: ...


PPrinterFactoryType = Callable[[str | None, str | None, str | None, str | None], PPrinterType]


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
def printer(request: SubRequest) -> Callable[[str, str | None], None]:
    """Pytest plugin to print test progress steps in verbose mode."""
    return _create_printer(request)


@pytest.fixture(scope="session", name="printer_session")
def printer_session(request: SubRequest) -> Callable[[str, str | None], None]:
    return _create_printer(request)


@pytest.fixture(scope="session")
def pprinter(request: SubRequest) -> Callable[[str, str | None], None]:
    """Pytest plugin to print test progress steps in verbose mode."""
    return _create_printer(request, " " * 2, "⏩", " ", "")


@pytest.fixture(scope="session")
def pprinter_factory(
    request: SubRequest,
) -> PPrinterFactoryType:
    def factory(
        icon: str | None = None, head: str | None = None, space: str | None = None, first: str | None = None
    ) -> PPrinterType:
        return _create_printer(request, head, icon, space, first)

    return factory


def _create_printer(
    request: SubRequest,
    head: str | None = None,
    icon: str | None = None,
    space: str | None = None,
    first: str | None = None,
) -> PPrinterType:
    if request.config.getoption("pytest_print_on") or request.config.getoption("verbose") > 0:
        terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
        capture_manager = request.config.pluginmanager.getplugin("capturemanager")
        if terminal_reporter is not None:  # pragma: no branch
            fmt = RecordFormatter(head=head, icon=icon, space=space, first=first)  # type: ignore # noqa: PGH003
            return State(
                terminal_reporter,
                capture_manager,
                fmt,
                _start=default_timer() if request.config.getoption("pytest_print_relative_time") else None,
            )

    return NoOpState()


@dc.dataclass(slots=True)
class RecordFormatter:
    # this is the complete message line
    head: str = "\t"
    icon: str = ""
    space: str = ""
    first: str = ""

    def __post_init__(self) -> None:
        for field in dc.fields(self):
            if getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

    @property
    def pre(self) -> str:
        return f"{self.head}{self.icon}{self.space}"


@dc.dataclass(slots=True)
class NoOpState:
    parent: NoOpState | None = None

    def __call__(self, msg: str, icon: str | None = None) -> None:
        """Do nothing."""

    @staticmethod
    def subprinter(_icon: str | None = None) -> NoOpState:
        return NoOpState()


@dc.dataclass(slots=True)
class State:
    _reporter: TerminalReporter
    _capture_manager: CaptureManager

    fmt: RecordFormatter
    level: int = 0

    # this will be set depending on print_relative
    _start: float | None = None
    parent: NoOpState | State | None = None

    @property
    def elapsed(self) -> float | None:
        if self._start is None:
            return None  # pragma: no cover
        return default_timer() - self._start

    def __call__(self, msg: str, icon: str | None = None) -> None:
        fmt = self.fmt if icon is None else dc.replace(self.fmt, icon=icon)

        timer = f"{self.elapsed}\t" if self.elapsed else ""
        indent = (" " * len(fmt.first) if self.level else fmt.first) + " " * self.level * len(fmt.pre)
        msg = f"{indent}{fmt.pre}{timer}{msg}"
        with self._capture_manager.global_and_fixture_disabled():
            self._reporter.write_line(msg)

    def subprinter(self, icon: str | None = None) -> State:
        fmt = dc.replace(self.fmt, icon=icon)  # type: ignore # noqa: PGH003
        return self.__class__(self._reporter, self._capture_manager, fmt, self.level + 1, self._start, self)


__all__ = [
    "__version__",
]
