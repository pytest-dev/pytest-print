from __future__ import annotations

import re
from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def extract_printer_text(lines: list[str]) -> str:
    output = "\n".join(line for line in lines if not line.startswith("=" * 20))
    output = output[output.find("test_a.py::") :]
    output = re.sub(r"\s*\[\s*\d+%\]", "", output)
    output = output.replace("test_a::", "a::")
    return re.sub(r"[ \t]+\n", "\n", output)


def seed_test(filename: str, pytester: pytest.Pytester) -> pytest.Pytester:
    src = Path(__file__).parent / filename
    assert src.exists()
    copy2(src, pytester.path / "test_a.py")
    return pytester


__all__ = [
    "extract_printer_text",
    "seed_test",
]
