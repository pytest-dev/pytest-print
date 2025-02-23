from __future__ import annotations

from typing import Callable


def test_pprinter_usage(pprinter: Callable[[str, str | None], None]) -> None:
    pprinter("start here the test start")

    printer1 = pprinter.subprinter("🚀")
    printer1("start a sub printer")

    printer2 = printer1.subprinter("🧹")
    printer2("start a sub sub printer")
    printer2("a message with a twist", "🔄")
    printer2("end a sub sub printer")

    printer1("end a sub printer")

    pprinter("end here the test end")
