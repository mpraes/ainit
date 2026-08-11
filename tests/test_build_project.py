from collections.abc import Callable
from pathlib import Path

import pytest

from ainit.choices import ProjectChoices
from ainit.generator import build_project, write_agent_rules


class FakeUvRunner:
    """Named fake that records uv invocations instead of shelling out."""

    def __init__(self) -> None:
        self.calls: list[tuple[list[str], Path]] = []

    def __call__(self, args: list[str], cwd: Path) -> None:
        self.calls.append((args, cwd))
        if args[:1] == ["init"]:
            (cwd / "pyproject.toml").write_text(
                '[project]\nname = "tmp"\nversion = "0.1.0"\n',
                encoding="utf-8",
            )


def test_write_agent_rules_all_creates_three_files(
    tmp_path: Path,
    make_choices: Callable[..., ProjectChoices],
) -> None:
    write_agent_rules(tmp_path, make_choices(agent_rules="All"))
    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / ".cursorrules").is_file()


def test_write_agent_rules_none_skips_files(
    tmp_path: Path,
    make_choices: Callable[..., ProjectChoices],
) -> None:
    write_agent_rules(tmp_path, make_choices(agent_rules="None"))
    assert list(tmp_path.iterdir()) == []


def test_build_project_writes_layout_without_real_uv(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    make_choices: Callable[..., ProjectChoices],
) -> None:
    fake_uv = FakeUvRunner()
    monkeypatch.setattr("ainit.generator._run_uv", fake_uv)

    folder = tmp_path / "demo"
    choices = make_choices(
        provider="DeepSeek",
        agent_rules="CLAUDE.md",
        linter="Ruff",
    )
    build_project(str(folder), choices)

    assert (folder / "main.py").is_file()
    assert (folder / "src" / "models" / "llm.py").is_file()
    assert (folder / "tests" / "test_smoke.py").is_file()
    assert (folder / "CLAUDE.md").is_file()
    assert not (folder / "AGENTS.md").exists()
    env_text = (folder / ".env").read_text(encoding="utf-8")
    assert "DEEPSEEK_API_KEY" in env_text
    pyproject = (folder / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.ruff]" in pyproject
    assert any(call[0][:1] == ["init"] for call in fake_uv.calls)
    assert any(call[0][:1] == ["add"] for call in fake_uv.calls)
