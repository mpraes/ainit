"""Project scaffolding: layout, deps, configs, and agent rules."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ainit.choices import ProjectChoices

_RUFF_TOML = """
[tool.ruff]
target-version = "py310"
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
"""

_PYRIGHT_TOML = """
[tool.pyright]
include = ["src"]
pythonVersion = "3.10"
typeCheckingMode = "basic"
"""

_SMOKE_PYTEST = """import os


def test_env_file_exists():
    assert os.path.exists(".env")


def test_llm_module_import():
    from src.models.llm import get_llm

    assert callable(get_llm)
"""

_SMOKE_UNITTEST = """import os
import unittest


class TestSmoke(unittest.TestCase):
    def test_env_file_exists(self):
        self.assertTrue(os.path.exists(".env"))

    def test_llm_module_import(self):
        from src.models.llm import get_llm

        self.assertTrue(callable(get_llm))


if __name__ == "__main__":
    unittest.main()
"""

_LLM_PY = '''import os

from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """Return the initialized LLM client."""
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
        or os.getenv("GROQ_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )
    if not api_key:
        raise ValueError("API key is not configured in the .env file")
    return {"status": "configured", "api_key_present": True}
'''

_MAIN_PY = """from src.models.llm import get_llm


def main():
    print("🤖 Agent project initialized successfully!")
    client = get_llm()
    print("Model status:", client)


if __name__ == "__main__":
    main()
"""

_FRAMEWORK_PKGS: dict[str, list[str]] = {
    "LangChain": ["langchain", "langchain-core"],
    "LangGraph": ["langgraph", "langchain-core"],
    "Deep Agents": ["deepagents"],
    "CrewAI": ["crewai"],
    "PydanticAI": ["pydantic-ai"],
    "Microsoft Agent Framework": ["agent-framework"],
    "LlamaIndex": ["llama-index", "llama-index-workflows"],
    "Google ADK": ["google-adk"],
    "OpenAI Agents SDK": ["openai-agents"],
    "None": [],
}

_PROVIDER_PKGS: dict[str, list[str]] = {
    "OpenAI": ["openai"],
    "Anthropic": ["anthropic"],
    "Groq": ["groq"],
    "DeepSeek": ["openai"],
    "Gemini": ["google-genai"],
    "Multi-Provider": ["openai", "anthropic", "google-genai"],
}

_LANGCHAIN_PROVIDER_PKGS: dict[str, list[str]] = {
    "OpenAI": ["langchain-openai"],
    "Anthropic": ["langchain-anthropic"],
    "Groq": ["langchain-groq"],
    "DeepSeek": ["langchain-openai"],
    "Gemini": ["langchain-google-genai"],
    "Multi-Provider": [
        "langchain-openai",
        "langchain-anthropic",
        "langchain-google-genai",
    ],
}

_LC_FAMILY = {"LangChain", "LangGraph", "Deep Agents"}

_PROVIDER_ENV: dict[str, str] = {
    "OpenAI": "OPENAI_API_KEY=your_key_here\n",
    "Anthropic": "ANTHROPIC_API_KEY=your_key_here\n",
    "Groq": "GROQ_API_KEY=your_key_here\n",
    "DeepSeek": "DEEPSEEK_API_KEY=your_key_here\n",
    "Gemini": "GOOGLE_API_KEY=your_key_here\n",
    "Multi-Provider": (
        "OPENAI_API_KEY=your_key_here\n"
        "ANTHROPIC_API_KEY=your_key_here\n"
        "GOOGLE_API_KEY=your_key_here\n"
    ),
}

_SRC_SUBDIRS = ("agent", "tools", "models", "prompts", "storage", "utils", "api")


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def provider_pkgs(framework: str, provider: str) -> list[str]:
    """Resolve provider packages, plus LangChain adapters when needed.

    Example:
        provider_pkgs("LangGraph", "Gemini")
        # ["google-genai", "langchain-google-genai"]
    """
    pkgs = list(_PROVIDER_PKGS.get(provider, []))
    if framework in _LC_FAMILY:
        pkgs.extend(_LANGCHAIN_PROVIDER_PKGS.get(provider, []))
    return _dedupe(pkgs)


def resolve_test_command(test_runner: str) -> str:
    """Return the single command used to run scaffold tests.

    Example:
        resolve_test_command("Pytest")  # "uv run pytest"
    """
    if test_runner == "unittest":
        return "uv run python -m unittest"
    return "uv run pytest"


def _run_uv(args: list[str], cwd: Path) -> None:
    subprocess.run(
        ["uv", *args],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def _append_pyproject(project_path: Path, block: str) -> None:
    pyproject = project_path / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    with pyproject.open("a", encoding="utf-8") as handle:
        if not text.endswith("\n"):
            handle.write("\n")
        handle.write(block)


def _rules_tooling_lines(config: ProjectChoices, test_cmd: str) -> list[str]:
    lines = [
        "# Agent rules",
        "",
        "Generated by [ainit](https://github.com/mpraes/ainit).",
        "",
        "## Package / commands",
        "",
        "- Always use `uv`, never `pip` or `pip install`.",
        "- Add deps: `uv add <pkg>` / `uv add --dev <pkg>`.",
        "- Run tools: `uv run <cmd>` (e.g. `uv run python main.py`).",
        f"- Tests: `{test_cmd}`.",
        "- Sync env: `uv sync`.",
    ]
    if config["linter"] == "Ruff":
        lines += [
            "- Lint: `uv run ruff check .`",
            "- Format: `uv run ruff format .`",
        ]
    if "Pyright" in config["type_check"]:
        lines += [
            "- Type check: `uv run basedpyright` "
            "(Pylance reads `[tool.pyright]` in the editor).",
        ]
    return lines


def _rules_style_lines(test_cmd: str) -> list[str]:
    return [
        "",
        "## Do not",
        "",
        "- Create/activate a venv manually if `uv` already manages it.",
        "- Suggest `pip install -r requirements.txt`.",
        "- Commit `.env` or API keys.",
        "",
        "## Code style",
        "",
        "- Functions: 4-20 lines. Split if longer.",
        "- Files: under 500 lines. Split by responsibility.",
        "- Explicit types. Prefer early returns over deep nesting.",
        "- Write WHY comments, not WHAT.",
        "",
        "## Tests",
        "",
        f"- Run with: `{test_cmd}`.",
        "- Every new function gets a test. Bug fixes get a regression test.",
        "- Mock external I/O (API, DB, filesystem).",
        "",
    ]


def agent_rules_body(config: ProjectChoices) -> str:
    """Build agent-rules markdown for the selected tooling.

    Example:
        text = agent_rules_body(choices)
    """
    test_cmd = resolve_test_command(config["test_runner"])
    lines = _rules_tooling_lines(config, test_cmd)
    lines += _rules_style_lines(test_cmd)
    return "\n".join(lines)


def _agent_rule_targets(choice: str) -> list[str]:
    if choice == "None":
        return []
    if choice == "All":
        return ["AGENTS.md", "CLAUDE.md", ".cursorrules"]
    return [choice]


def write_agent_rules(project_path: Path, config: ProjectChoices) -> None:
    """Write selected agent rule files into the project root.

    Example:
        write_agent_rules(Path("my_app"), choices)
    """
    body = agent_rules_body(config)
    for name in _agent_rule_targets(config["agent_rules"]):
        (project_path / name).write_text(body, encoding="utf-8")


def _create_layout(project_path: Path) -> None:
    project_path.mkdir(parents=True, exist_ok=True)
    for subdir in _SRC_SUBDIRS:
        folder = project_path / "src" / subdir
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "__init__.py").touch()
    tests = project_path / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "__init__.py").touch()


def _storage_pkgs(storage: str) -> list[str]:
    if storage == "Qdrant":
        return ["qdrant-client"]
    if storage == "PostgreSQL":
        return ["psycopg2-binary", "pgvector", "sqlalchemy"]
    if storage == "Redis":
        return ["redis"]
    return []


def _observability_pkgs(logging: str) -> list[str]:
    if logging == "LangSmith":
        return ["langsmith"]
    if logging == "Arize":
        return ["arize-phoenix"]
    if logging == "Loguru":
        return ["loguru"]
    return []


def runtime_packages(config: ProjectChoices) -> list[str]:
    """Collect runtime packages for the selected stack.

    Example:
        runtime_packages(choices)
    """
    pkgs = ["pydantic", "pydantic-settings", "python-dotenv"]
    pkgs.extend(_FRAMEWORK_PKGS.get(config["framework"], []))
    pkgs.extend(provider_pkgs(config["framework"], config["provider"]))
    pkgs.extend(_storage_pkgs(config["storage"]))
    pkgs.extend(_observability_pkgs(config["logging"]))
    return _dedupe(pkgs)


def dev_packages(config: ProjectChoices) -> list[str]:
    """Collect development packages for tests/lint/types.

    Example:
        dev_packages(choices)
    """
    pkgs: list[str] = []
    if config["test_runner"] == "Pytest":
        pkgs.extend(["pytest", "pytest-asyncio"])
    if config["linter"] == "Ruff":
        pkgs.append("ruff")
    if "Pyright" in config["type_check"]:
        pkgs.append("basedpyright")
    return pkgs


def _install_packages(
    project_path: Path,
    runtime: list[str],
    dev: list[str],
) -> None:
    _run_uv(["init"], project_path)
    if runtime:
        _run_uv(["add", *runtime], project_path)
    if dev:
        _run_uv(["add", "--dev", *dev], project_path)


def _write_tool_configs(project_path: Path, config: ProjectChoices) -> None:
    if config["linter"] == "Ruff":
        _append_pyproject(project_path, _RUFF_TOML)
    if "Pyright" in config["type_check"]:
        _append_pyproject(project_path, _PYRIGHT_TOML)


def _write_env_file(project_path: Path, provider: str) -> None:
    content = "# API keys and settings generated by ainit\n"
    content += _PROVIDER_ENV.get(provider, "")
    (project_path / ".env").write_text(content, encoding="utf-8")


def _write_entrypoints(project_path: Path, test_runner: str) -> None:
    (project_path / "src" / "models" / "llm.py").write_text(_LLM_PY, encoding="utf-8")
    (project_path / "main.py").write_text(_MAIN_PY, encoding="utf-8")
    smoke = _SMOKE_UNITTEST if test_runner == "unittest" else _SMOKE_PYTEST
    (project_path / "tests" / "test_smoke.py").write_text(smoke, encoding="utf-8")


def build_project(folder_name: str, config: ProjectChoices) -> None:
    """Scaffold a new AI agent project from interactive choices.

    Example:
        build_project("my_agent", prompt_choices())
    """
    project_path = Path(folder_name).resolve()
    _create_layout(project_path)
    _install_packages(
        project_path,
        runtime_packages(config),
        dev_packages(config),
    )
    _write_tool_configs(project_path, config)
    _write_env_file(project_path, config["provider"])
    _write_entrypoints(project_path, config["test_runner"])
    write_agent_rules(project_path, config)
