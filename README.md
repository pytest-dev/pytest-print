# pytest-print

[![PyPI](https://img.shields.io/pypi/v/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![Downloads](https://static.pepy.tech/badge/pytest-print/month)](https://pepy.tech/project/pytest-print)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-print?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/pytest-dev/pytest-print/actions/workflows/check.yaml/badge.svg)](https://github.com/pytest-dev/pytest-print/actions/workflows/check.yaml)

Allows to print extra content onto the PyTest reporting. This can be used for example to report sub-steps for long
running tests, or to print debug information in your tests when you cannot debug the code.

## install

```sh
pip install pytest-print
```

The plugin provides ability to print information during the tests runs.

## flags

- `--print` by default the module activates print when pytest verbosity is greater than zero, this allows to bypass this
  and force print irrespective of the verbosity
- `--print-relative-time` will print the relative time since the start of the test (display how long it takes to reach
  prints)

## use cases

### sub-step reporting

For tests that are long running this can provide feedback to the end-user that what is just happening in the background.

```python
def test_server_parallel_requests(printer, tmpdir):
    printer("create virtual environment into {}".format(tmpdir))
    create_virtual_environment(tmpdir)

    printer("start server from virtual env")
    start_server(tmpdir)

    printer("do the parallel request test")
    parallel_requests()
```

```bash
$ py.test --vv
============================= test session starts ==============================
platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
collecting ... collected 1 item

test_printer_progress.py::test_server_parallel_requests
    create virtual environment
    start server from virtual env
    do the parallel request test
PASSED                                                                   [100%]

=========================== 1 passed in 0.02 seconds ===========================
```

### factory tests

If you need nested messages you can use the `printer_factory` fixture or the `pprinter`.

```python
def test_pprinter_usage(pprinter):
    pprinter("start here the test start")

    printer1 = pprinter.subprinter("🚀")
    printer1("start a sub printer")

    printer2 = printer1.subprinter("🧹")
    printer2("start a sub sub printer")

    # you can override the `icon` on a per-message
    printer2("a message with a twist", "🔄")
    printer2("end a sub sub printer")

    printer1("end a sub printer")

    pprinter("end here the test end")
```

```bash
$ py.test --vv
============================= test session starts ==============================
platform linux -- Python 3.13.2, pytest-8.3.4, pluggy-1.5.0 -- .venv/bin/python3.13
cachedir: .pytest_cache
rootdir: /home/users/antonio/Projects/github/pytest-print
configfile: pyproject.toml
plugins: print-0.1.dev168+g4000034
collected 1 item

tests/example3.py::test_pprinter_usage
  ⏩ start here the test start
      🚀 start a sub printer
          🧹 start a sub sub printer
          🔄 a message with a twist
          🧹 end a sub sub printer
      🚀 end a sub printer
  ⏩ end here the test end

tests/example3.py::test_pprinter_usage PASSED                            [100%]

============================== 1 passed in 0.01s ===============================
```
