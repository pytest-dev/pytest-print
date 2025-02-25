from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Iterator

import pytest

if TYPE_CHECKING:
    from pytest_print import Printer


def create_virtual_environment() -> None:
    sleep(0.001)


def start_server() -> None:
    sleep(0.001)


def parallel_requests() -> None:
    sleep(0.001)


@pytest.fixture(scope="session")
def _expensive_setup(printer_session: Printer) -> Iterator[None]:
    printer_session("attempt global peace")
    yield
    printer_session("teardown global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_global_peace(printer_session: Printer) -> None:
    printer_session("here we have global peace")


@pytest.mark.usefixtures("_expensive_setup")
def test_server_parallel_requests(printer: Printer) -> None:
    printer("create virtual environment")
    create_virtual_environment()

    printer("start server from virtual env")
    start_server()

    printer("do the parallel request test")
    parallel_requests()
