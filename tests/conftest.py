from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.monkeypatch import MonkeyPatch

pytest_plugins = ["pytester"]


@pytest.fixture
def example(request: SubRequest, testdir: pytest.Testdir, monkeypatch: MonkeyPatch) -> pytest.Testdir:
    monkeypatch.setattr("_pytest._io.terminalwriter.get_terminal_width", lambda: 80)
    monkeypatch.setenv("COLUMNS", str(80))
    source = Path(request.module.__file__).parent / request.module.EXAMPLE
    dest = Path(str(testdir.tmpdir)) / f"test_{request.module.EXAMPLE}"
    copy2(str(source), str(dest))
    return testdir
