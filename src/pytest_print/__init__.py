# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime
from typing import Text

import pytest
import six
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution


def _version():  # type: () -> Text
    try:
        return six.text_type(get_distribution(__name__).version)
    except DistributionNotFound:  # pragma: no cover
        return '0.0.0-dev'  # pragma: no cover


#: Semantic Version of the module.
__version__ = _version()


# noinspection SpellCheckingInspection
def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--print-relative-time',
                    action='store_true',
                    dest="pytest_print_relative_time",
                    default=False,
                    help="Time in milliseconds when the print was invoked,"
                         " relative to the time the fixture was created.")


# noinspection SpellCheckingInspection
@pytest.fixture
def printer(request):
    """pytest plugin to print test progress steps in verbose mode"""

    # noinspection PyUnusedLocal
    def no_op(*args):
        """do nothing"""

    if request.config.getoption('verbose') <= 0:
        return no_op

    terminal_reporter = request.config.pluginmanager.getplugin('terminalreporter')
    if terminal_reporter is None:
        return no_op  # pragma: no cover

    print_relative_time = request.config.getoption('pytest_print_relative_time')

    first_call = [True]
    start_datetime = datetime.now()

    def _print(msg):

        if first_call[0]:  # in case of the first call we don't have a new empty line, print it
            terminal_reporter.write('\n')
            first_call[0] = False

        terminal_reporter.write('\t')

        if print_relative_time:
            delta = datetime.now() - start_datetime
            terminal_reporter.write(delta.total_seconds())
            terminal_reporter.write('\t')

        terminal_reporter.write(msg)
        terminal_reporter.write('\n')

    return _print
