from __future__ import absolute_import, unicode_literals

from datetime import datetime

import pytest

from .version import __version__


# noinspection SpellCheckingInspection
def pytest_addoption(parser):
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


# noinspection SpellCheckingInspection
@pytest.fixture(name="printer", scope="function")
def printer(request):
    """pytest plugin to print test progress steps in verbose mode"""
    return create_printer(request)


@pytest.fixture(scope="session", name="printer_session")
def printer_session(request):
    return create_printer(request)


def create_printer(request):
    if request.config.getoption("pytest_print_on") or request.config.getoption("verbose") > 0:
        terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
        if terminal_reporter is not None:
            state = State(request.config.getoption("pytest_print_relative_time"), terminal_reporter)
            return state.printer

    return no_op


# noinspection PyUnusedLocal
def no_op(msg):
    """Do nothing"""


class State(object):
    def __init__(self, print_relative, reporter):
        self._reporter = reporter
        self._start = datetime.now() if print_relative else None
        self._print_relative = print_relative

    @property
    def elapsed(self):
        if self._start is None:
            return None
        return (datetime.now() - self._start).total_seconds()

    def printer(self, msg):
        msg = "\t{}{}".format("{}\t".format(self.elapsed) if self._print_relative else "", msg)
        self._reporter.write_line(msg)

    def __repr__(self):
        return "{}(print_relative={}, reporter={!r})".format(type(self).__name__, self._print_relative, self._reporter)

    __slots__ = ("_start", "_print_relative", "_reporter")


__all__ = ("__version__",)
