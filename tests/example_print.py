from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytest_print import Printer


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
    printer("start server from virtual env")
    printer("do the parallel request test")
