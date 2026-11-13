from __future__ import annotations

import pickle  # ruff: ignore[suspicious-pickle-import]  # test trusted class serialization

import pytest

import pytest_print


@pytest.mark.parametrize("name", ["Formatter", "PrettyPrinter", "PrettyPrinterFactory", "Printer"])
def test_public_type_identity(name: str) -> None:
    public_type = getattr(pytest_print, name)
    assert public_type.__module__ == "pytest_print"
    assert pickle.loads(pickle.dumps(public_type)) is public_type  # ruff: ignore[suspicious-pickle-usage]  # trusted data


def test_public_exports() -> None:
    assert set(pytest_print.__all__) == {"Formatter", "PrettyPrinter", "PrettyPrinterFactory", "Printer"}
