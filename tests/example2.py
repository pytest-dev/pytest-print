from __future__ import annotations

from time import sleep
from typing import Callable, Iterator

import pytest


def create_virtual_environment() -> None:
    sleep(0.001)


def start_server() -> None:
    sleep(0.001)


def parallel_requests() -> None:
    sleep(0.001)


@pytest.fixture(scope="session")
def pprinter_session(printer_factory: Callable) -> Callable[[str], None]:
    return printer_factory("⏩", "  ", " ", "")


@pytest.fixture(name="pprinter")
def pprinter(pprinter_session: Callable) -> Callable[[str], None]:
    return pprinter_session.subprinter("🚀")


@pytest.fixture(scope="session")
def _expensive_setup(pprinter_session: Callable[[str], None]) -> Iterator[None]:
    pprinter_session("attempt global peace")
    yield
    pprinter_session("teardown global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_global_peace(pprinter_session: Callable[[str], None]) -> None:
    pprinter_session("here we have global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_server_parallel_requests(pprinter: Callable[[str], None]) -> None:
    pprinter("create virtual environment")
    create_virtual_environment()

    pprinter("start server from virtual env")
    start_server()

    pprinter("do the parallel request test")
    parallel_requests()


def test_printer_factory_usage(printer_factory: Callable[[str, str | None], None]) -> None:
    printer = printer_factory("⏩", "  ", " ", "")
    printer("start here the test start")

    printer1 = printer.subprinter("🚀")
    printer1("start a sub printer")

    printer2 = printer1.subprinter("🧹")
    printer2("start a sub sub printer")
    printer2("a message with a twist", "🔄")
    printer2("end a sub sub printer")

    printer1("end a sub printer")

    printer("end here the test end")
