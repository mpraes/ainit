from collections.abc import Callable

import pytest

from ainit.choices import ProjectChoices


@pytest.fixture
def make_choices() -> Callable[..., ProjectChoices]:
    def _make(**overrides: str) -> ProjectChoices:
        choices: ProjectChoices = {
            "framework": "None",
            "provider": "Gemini",
            "storage": "None",
            "logging": "None",
            "test_runner": "Pytest",
            "linter": "Ruff",
            "type_check": "None",
            "agent_rules": "AGENTS.md",
        }
        for key, value in overrides.items():
            if key not in choices:
                raise KeyError(
                    f"Unknown choice key {key!r}; expected one of {sorted(choices)}"
                )
            choices[key] = value  # type: ignore[literal-required]
        return choices

    return _make
