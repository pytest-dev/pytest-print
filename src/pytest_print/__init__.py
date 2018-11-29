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
@pytest.fixture
def printer(request):
    """pytest plugin to print test progress steps in verbose mode"""

    # noinspection PyUnusedLocal
    def no_op(*args):
        """do nothing"""

    if not request.config.getoption("pytest_print_on") and request.config.getoption("verbose") <= 0:
        return no_op

    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is None:
        return no_op  # pragma: no cover

    print_relative_time = request.config.getoption("pytest_print_relative_time")

    first_call = [True]
    start_datetime = datetime.now()

    def _print(msg):

        if first_call[0]:  # in case of the first call we don't have a new empty line, print it
            terminal_reporter.write("\n")
            first_call[0] = False

        terminal_reporter.write("\t")

        if print_relative_time:
            delta = datetime.now() - start_datetime
            terminal_reporter.write(delta.total_seconds())
            terminal_reporter.write("\t")

        terminal_reporter.write(msg)
        terminal_reporter.write("\n")

    return _print


__all__ = ("__version__",)
