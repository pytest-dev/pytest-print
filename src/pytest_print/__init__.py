"""Pytest print functionality."""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from timeit import default_timer
from typing import TYPE_CHECKING, Protocol, TypeVar, cast

import pytest

if TYPE_CHECKING:
    from _pytest.capture import CaptureManager
    from _pytest.fixtures import SubRequest
    from _pytest.terminal import TerminalReporter


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--print",
        action="store_true",
        dest="pytest_print_on",
        default=False,
        help="By default the plugins if verbosity is greater than zero (-v flag), this forces on",
    )
    group.addoption(
        "--print-relative-time",
        action="store_true",
        dest="pytest_print_relative_time",
        default=False,
        help="Time in milliseconds when the print was invoked, relative to the time the fixture was created.",
    )


class Printer(Protocol):
    """Printer within a pytest session."""

    def __call__(self, msg: str) -> None:
        """
        Print the given message.

        :param msg: message to print
        """


@pytest.fixture(scope="session")
def printer_session(request: SubRequest) -> Printer:
    """Pytest plugin to print test progress steps in verbose mode (session scoped)."""
    return _create(request, _Printer, Formatter())


@pytest.fixture(name="printer")
def printer(printer_session: Printer) -> Printer:
    """Pytest plugin to print test progress steps in verbose mode."""
    return printer_session


class PrettyPrinter(Protocol):
    """Printer within a pytest session."""

    def __call__(self, msg: str, *, icon: str | None = None) -> None:
        """
        Print the given message in pretty mode.

        :param msg: message to print
        :param icon: icon to use, will use the one configured at printer creation
        """

    def indent(self, *, icon: str) -> PrettyPrinter:
        """
        Create an indented pretty printer.

        :param icon: change the icon from the parents printer
        """


@pytest.fixture(scope="session")
def pretty_printer(request: SubRequest) -> PrettyPrinter:
    """Pytest plugin to print test progress steps in verbose mode."""
    formatter = Formatter(head=" ", icon="⏩", space=" ", indentation="  ", timer_fmt="[{elapsed:.20f}]")
    return _create(request, _PrettyPrinter, formatter)


class PrettyPrinterFactory(Protocol):
    """Create a new pretty printer."""

    def __call__(self, *, formatter: Formatter) -> PrettyPrinter:
        """
        Create a new pretty printer.

        :param formatter: the formatter to use with this printer
        """


@pytest.fixture(scope="session")
def create_pretty_printer(request: SubRequest) -> PrettyPrinterFactory:
    """Pytest plugin to print test progress steps in verbose mode."""
    Formatter(head=" ", icon="⏩", space=" ", indentation="  ", timer_fmt="[{elapsed:.20f}]")

    def meth(*, formatter: Formatter) -> PrettyPrinter:
        return _create(request, _PrettyPrinter, formatter)

    return meth


@dataclass(frozen=True, **{"slots": True, "kw_only": True} if sys.version_info >= (3, 10) else {})
class Formatter:
    """Configures how to format messages to be printed."""

    head: str = ""  #: start every line with this prefix
    icon: str = ""  #: an icon text printed immediately after the head
    space: str = ""  #: character to print right after the prefix
    indentation: str = "\t"  #: use this character to indent the message, only useful for indented printers
    timer_fmt: str = "{elapsed}\t"  #: how to print out elapsed time since the creation of the printer - float (seconds)

    @property
    def _pre(self) -> str:
        return f"{self.head}{self.icon}{self.space}"

    def __call__(self, msg: str, level: int, elapsed: float | None) -> str:
        """
        Format the given message.

        :param msg: the message to format
        :param level: indentation level
        :param elapsed: time elapsed
        :return: the formatted message
        """
        indentation = " " * (len(self.indentation)) if level else self.indentation
        spacer = " " * len(self._pre) * level
        timer = self.timer_fmt.format(elapsed=elapsed) if elapsed else ""
        return f"{indentation}{timer}{spacer}{self._pre}{msg}"


class _Printer:
    def __init__(
        self,
        *,
        reporter: TerminalReporter | None,
        capture_manager: CaptureManager | None,
        formatter: Formatter,
        level: int,
        start: float | None,
    ) -> None:
        self._reporter = reporter
        self._capture_manager = capture_manager
        self._formatter = formatter
        self._level = level
        self._start = start

    def __call__(self, msg: str) -> None:
        self._print(msg, self._formatter)

    def _print(self, msg: str, formatter: Formatter) -> None:
        if self._reporter is None or self._capture_manager is None:  # disabled
            return
        msg = formatter(msg, self._level, None if self._start is None else default_timer() - self._start)
        with self._capture_manager.global_and_fixture_disabled():
            self._reporter.write_line(msg)


class _PrettyPrinter(_Printer):
    def __call__(self, msg: str, *, icon: str | None = None) -> None:
        self._print(msg, self._formatter if icon is None else replace(self._formatter, icon=icon))

    def indent(self, *, icon: str) -> PrettyPrinter:
        return _PrettyPrinter(
            reporter=self._reporter,
            capture_manager=self._capture_manager,
            formatter=replace(self._formatter, icon=icon),
            level=self._level + 1,
            start=self._start,
        )


_OfType = TypeVar("_OfType", bound=_Printer)


def _create(request: SubRequest, of_type: type[_OfType], formatter: Formatter) -> _OfType:
    return of_type(
        reporter=cast("TerminalReporter | None", request.config.pluginmanager.getplugin("terminalreporter"))
        if request.config.getoption("pytest_print_on") or cast("int", request.config.getoption("verbose")) > 0
        else None,
        capture_manager=cast("CaptureManager | None", request.config.pluginmanager.getplugin("capturemanager")),
        formatter=formatter,
        start=default_timer() if request.config.getoption("pytest_print_relative_time") else None,
        level=0,
    )


__all__ = [
    "Formatter",
    "PrettyPrinter",
    "PrettyPrinterFactory",
    "Printer",
]
