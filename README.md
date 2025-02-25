# pytest-print

[![PyPI](https://img.shields.io/pypi/v/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-print?style=flat-square)](https://pypi.org/project/pytest-print)
[![Downloads](https://static.pepy.tech/badge/pytest-print/month)](https://pepy.tech/project/pytest-print)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-print?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/pytest-dev/pytest-print/actions/workflows/check.yaml/badge.svg)](https://github.com/pytest-dev/pytest-print/actions/workflows/check.yaml)

Allows to print extra content onto the PyTest reporting. This can be used for example to report sub-steps for long
running tests, or to print debug information in your tests when you cannot debug the code (so that the end user does not
need to wonder if the test froze/dead locked or not).

<!--ts-->

- [Install](#install)
- [CLI flags](#cli-flags)
- [API](#api)
  - [Example: printer_session](#example-printer_session)
  - [Example: pretty_printer](#example-pretty_printer)
  - [Example: create_pretty_printer](#example-create_pretty_printer)

<!--te-->

## Install

```sh
pip install pytest-print
```

## CLI flags

The following flags are registered for the pytest command:

- `--print` by default the module activates print when pytest verbosity is greater than zero, this allows to bypass this
  and force print irrespective of the verbosity
- `--print-relative-time` will print the relative time since the start of the test (display how long it takes to reach
  prints)

## API

This library provides the following fixtures that help you print messages within a pytest run (bypasses the pytest
output capture, so it will show up in the standard output, even if the test passes):

- `printer: Printter` - function level fixture, when called prints a message line (with very simple formatting),
- [`printer_session: Printter`](#example-printer_session) - session scoped fixture same as above but using (this exists
  as a backwards compatibility layer, as we didn't want to switch the originally function scope variant to session one),
- [`pretty_printer: PrettyPrintter`](#example-pretty_printer) - session scoped fixture, when called prints a message
  line (with fancy formatting of space for indentation, `⏩` icon for every message, and elapsed time format in form of
  `[{elapsed:.20f}]`) and also allows creating a printer that will be indented one level deeper (and optionally use a
  different icon).
- [`create_pretty_printer: PrettyPrinterFactory`](#example-create_pretty_printer) - allows the caller to customize the
  fancy formatter as they wish. Takes one `formatter` argument, whose arguments should be interpreted as:

  ```shell
  ┌──────┐   ┌──────────┐┌─────────┐┌────────┐
  │ pre  │ ==│   head   ││  icon   ││ space  │
  └──────┘   └──────────┘└─────────┘└────────┘

  ┌─────────────┐┌───────┐┌──────┐┌────────────┐
  │ indentation ││ timer ││ pre  ││ msg        │
  └─────────────┘└───────┘└──────┘└────────────┘
                 ┌───────┐┌────────────────────┐┌──────┐┌────────────┐
                 │ timer ││ spacer             ││ pre  ││ msg        │
                 └───────┘└────────────────────┘└──────┘└────────────┘
                 ┌───────┐┌────────────────────┐┌────────────────────┐┌──────┐┌────────────┐
                 │ timer ││ spacer             ││ spacer             ││ pre  ││ msg        │
                 └───────┘└────────────────────┘└────────────────────┘└──────┘└────────────┘
  ```

### Example: `printer_session`

```python
from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import pytest

if TYPE_CHECKING:
    from pytest_print import Printer


@pytest.fixture(scope="session")
def _expensive_setup(printer_session: Printer) -> Iterator[None]:
    printer_session("setup")
    yield
    printer_session("teardown")


@pytest.mark.usefixtures("_expensive_setup")
def test_run(printer_session: Printer) -> None:
    printer_session("running")
```

```shell
pytest magic.py -vvvv
...

magic.py::test_run
        setup expensive operation
        running test

magic.py::test_run PASSED
        teardown expensive operation
```

### Example: `pretty_printer`

```python
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pytest_print import Formatter

if TYPE_CHECKING:
    from pytest_print import PrettyPrinter, PrettyPrinterFactory


@pytest.fixture(scope="session")
def pretty(create_pretty_printer: PrettyPrinterFactory) -> PrettyPrinter:
    formatter = Formatter(indentation="  ", head=" ", space=" ", icon="⏩", timer_fmt="[{elapsed:.20f}]")
    return create_pretty_printer(formatter=formatter)


def test_long_running(pretty: PrettyPrinter) -> None:
    pretty("Starting test")

    pretty_printer_1 = pretty.indent(icon="🚀")
    pretty_printer_1("Drill down to 1st level details")

    pretty_printer_2 = pretty_printer_1.indent(icon="🚀")
    pretty_printer_2("Drill down to 2nd level details")

    pretty("Finished test")
```

```shell
magic.py::test_long_running
   ⏩ Starting test
      🚀 Drill down to 1st level details
         🚀 Drill down to 2nd level details
   ⏩ Finished test

magic.py::test_long_running PASSED
```

### Example: `create_pretty_printer`

If you need nested messages you can use the `printer_factory` fixture or the `pprinter`.

```python
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pytest_print import Formatter

if TYPE_CHECKING:
    from pytest_print import PrettyPrinter, PrettyPrinterFactory


@pytest.fixture(scope="session")
def pretty(create_pretty_printer: PrettyPrinterFactory) -> PrettyPrinter:
    formatter = Formatter(
      indentation=" I ",
      head=" H ",
      space=" S ",
      icon="🧹",
      timer_fmt="[{elapsed:.5f}]",
     )
    return create_pretty_printer(formatter=formatter)


def test_long_running(pretty: PrettyPrinter) -> None:
    pretty("Starting test")

    pretty_printer_1 = pretty.indent(icon="🚀")
    pretty_printer_1("Drill down to 1st level details")

    pretty_printer_2 = pretty_printer_1.indent(icon="🚀")
    pretty_printer_2("Drill down to 2nd level details")

    pretty("Finished test")
```

```bash
pytest magic.py --print --print-relative-time
...

magic.py
 I [0.00022] H 🧹 S Starting test
   [0.00029]        H 🚀 S Drill down to 1st level details
   [0.00034]               H 🚀 S Drill down to 2nd level details
 I [0.00038] H 🧹 S Finished test
```
