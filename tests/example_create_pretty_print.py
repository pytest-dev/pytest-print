from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Iterator

import pytest

from pytest_print import Formatter

if TYPE_CHECKING:
    from pytest_print import PrettyPrinter, PrettyPrinterFactory


def create_virtual_environment() -> None:
    sleep(0.001)


def start_server() -> None:
    sleep(0.001)


def parallel_requests() -> None:
    sleep(0.001)


@pytest.fixture(scope="session")
def pretty(create_pretty_printer: PrettyPrinterFactory) -> PrettyPrinter:
    formatter = Formatter(indentation="  ", head=" ", space=" ", icon="⏩", timer_fmt="[{elapsed:.20f}]")
    return create_pretty_printer(formatter=formatter)


@pytest.fixture(name="pprinter", scope="session")
def pprinter(pretty: PrettyPrinter) -> PrettyPrinter:
    return pretty.indent(icon="🚀")


@pytest.fixture(scope="session")
def _expensive_setup(pretty: PrettyPrinter) -> Iterator[None]:
    pretty("attempt global peace")
    yield
    pretty("teardown global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_global_peace(pretty: PrettyPrinter) -> None:
    pretty("here we have global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_server_parallel_requests(pprinter: PrettyPrinter) -> None:
    pprinter("create virtual environment")
    create_virtual_environment()

    pprinter("start server from virtual env")
    start_server()

    pprinter("do the parallel request test")
    parallel_requests()


def test_create_pretty_printer_usage(create_pretty_printer: PrettyPrinterFactory) -> None:
    formatter = Formatter(icon="⏩", head=" ", space=" ", indentation="..", timer_fmt="[{elapsed:.20f}]")
    printer = create_pretty_printer(formatter=formatter)
    printer("start here the test start")

    printer1 = printer.indent(icon="🚀")
    printer1("start an indented printer")

    printer2 = printer1.indent(icon="🧹")
    printer2("start an indented indented printer")
    printer2("a message with a twist", icon="🔄")
    printer2("end an indented indented printer")

    printer1("end an indented printer")

    printer("end here the test end")
