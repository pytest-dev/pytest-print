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
    return _provide_printer(request)


@pytest.fixture(scope="session", name="printer_session")
def printer_session(request):
    return _provide_printer(request)


class State(object):
    def __init__(self, print_relative_time):
        self.first_call = True
        self.start_datetime = datetime.now() if print_relative_time else None
        self.print_relative_time = print_relative_time

    @property
    def elapsed(self):
        if self.start_datetime is None:
            return None
        return (datetime.now() - self.start_datetime).total_seconds()

    __slots__ = ("first_call", "start_datetime", "print_relative_time")


def _provide_printer(request):
    if request.config.getoption("pytest_print_on") and request.config.getoption("verbose") > 0:
        terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
        if terminal_reporter is not None:
            state = State(request.config.getoption("pytest_print_relative_time"))

            def _print(msg):
                if state.first_call:  # in case of the first call we don't have a new empty line, print it
                    state.first_call = False
                    terminal_reporter.write("\n")

                terminal_reporter.write("\t")

                if state.print_relative_time:
                    terminal_reporter.write(str(state.elapsed))
                    terminal_reporter.write("\t")

                terminal_reporter.write(msg)
                terminal_reporter.write("\n")

            return _print

    return lambda *args: None


__all__ = ("__version__",)
