from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_print import PrettyPrinter


def test_pprinter_usage(pretty_printer: PrettyPrinter) -> None:
    pretty_printer("start here the test start")

    printer1 = pretty_printer.indent(icon="🚀")
    printer1("start an indented printer")

    printer2 = printer1.indent(icon="🧹")
    printer2("start an indented indented printer")
    printer2("a message with a twist", icon="🔄")
    printer2("end an indented indented printer")

    printer1("end an indented printer")

    pretty_printer("end here the test end")
