from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Callable, Iterator

import pytest

if TYPE_CHECKING:
    from pytest_print import PPrinterFactoryType, PPrinterType


def create_virtual_environment() -> None:
    sleep(0.001)


def start_server() -> None:
    sleep(0.001)


def parallel_requests() -> None:
    sleep(0.001)


@pytest.fixture(scope="session")
def pprinter_session(pprinter_factory: PPrinterFactoryType) -> PPrinterType:
    return pprinter_factory(indentation="  ", head=" ", space=" ", icon="⏩", timerfmt="[{elapsed:.20f}]")


@pytest.fixture(name="pprinter")
def pprinter(pprinter_session: PPrinterType) -> PPrinterType:
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


def test_pprinter_factory_usage(pprinter_factory: PPrinterFactoryType) -> None:
    printer = pprinter_factory(icon="⏩", head=" ", space=" ", indentation="..", timerfmt="[{elapsed:.20f}]")
    printer("start here the test start")

    printer1 = printer.subprinter("🚀")
    printer1("start a sub printer")

    printer2 = printer1.subprinter("🧹")
    printer2("start a sub sub printer")
    printer2("a message with a twist", "🔄")
    printer2("end a sub sub printer")

    printer1("end a sub printer")

    printer("end here the test end")
