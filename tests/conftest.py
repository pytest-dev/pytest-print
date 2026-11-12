from __future__ import annotations

import re
from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

pytest_plugins: Final[list[str]] = ["pytester"]


@pytest.fixture(name="extract_printer_text")
def _extract_printer_text() -> Callable[[list[str]], str]:
    def extract(lines: list[str]) -> str:
        output = "\n".join(line for line in lines if not line.startswith("=" * 20))
        output = output[output.find("test_a.py::") :]
        output = re.sub(r"\s*\[\s*\d+%\]", "", output)
        output = output.replace("test_a::", "a::")
        return re.sub(r"[ \t]+\n", "\n", output)

    return extract


@pytest.fixture(name="seed_test")
def _seed_test(pytester: pytest.Pytester) -> Callable[[str], pytest.Pytester]:
    def seed(filename: str) -> pytest.Pytester:
        src = Path(__file__).parent / filename
        assert src.exists()
        copy2(src, pytester.path / "test_a.py")
        return pytester

    return seed
