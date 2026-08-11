from collections.abc import Callable

from ainit.choices import ProjectChoices
from ainit.generator import (
    agent_rules_body,
    dev_packages,
    provider_pkgs,
    resolve_test_command,
    runtime_packages,
)


def test_provider_pkgs_adds_langchain_adapter_for_lc_family() -> None:
    pkgs = provider_pkgs("LangGraph", "Gemini")
    assert pkgs == ["google-genai", "langchain-google-genai"]


def test_provider_pkgs_skips_langchain_adapter_without_framework() -> None:
    pkgs = provider_pkgs("None", "DeepSeek")
    assert pkgs == ["openai"]


def test_resolve_test_command_for_pytest_and_unittest() -> None:
    assert resolve_test_command("Pytest") == "uv run pytest"
    assert resolve_test_command("unittest") == "uv run python -m unittest"


def test_runtime_packages_include_framework_and_provider(
    make_choices: Callable[..., ProjectChoices],
) -> None:
    choices = make_choices(framework="OpenAI Agents SDK", provider="OpenAI")
    pkgs = runtime_packages(choices)
    assert "openai-agents" in pkgs
    assert "openai" in pkgs
    assert "langchain-openai" not in pkgs


def test_dev_packages_follow_tooling_flags(
    make_choices: Callable[..., ProjectChoices],
) -> None:
    choices = make_choices(
        test_runner="unittest",
        linter="Ruff",
        type_check="Pyright (Pylance-compatible)",
    )
    assert dev_packages(choices) == ["ruff", "basedpyright"]


def test_agent_rules_body_mentions_uv_and_ruff(
    make_choices: Callable[..., ProjectChoices],
) -> None:
    body = agent_rules_body(make_choices())
    assert "uv add" in body
    assert "uv run ruff check ." in body
    assert "uv run pytest" in body
    assert "never `pip`" in body or "Never `pip`" in body or "pip install" in body
