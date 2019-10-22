from time import sleep


def create_virtual_environment():
    sleep(0.001)


def start_server():
    sleep(0.001)


def parallel_requests():
    sleep(0.001)


def test_server_parallel_requests(printer, tmpdir):
    printer("create virtual environment")
    create_virtual_environment()

    printer("start server from virtual env")
    start_server()

    printer("do the parallel request test")
    parallel_requests()
