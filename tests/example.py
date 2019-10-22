from time import sleep

import pytest


def create_virtual_environment():
    sleep(0.001)


def start_server():
    sleep(0.001)


def parallel_requests():
    sleep(0.001)


@pytest.fixture(scope="session")
def expensive_setup(printer_session):
    printer_session("attempt global peace")
    yield
    printer_session("teardown global peace")


def test_global_peace(printer_session, expensive_setup):
    printer_session("here we have global peace")


def test_server_parallel_requests(printer, tmpdir, expensive_setup):
    printer("create virtual environment")
    create_virtual_environment()

    printer("start server from virtual env")
    start_server()

    printer("do the parallel request test")
    parallel_requests()
