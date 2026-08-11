<div align="center">

<pre>
 █████╗ ██╗███╗   ██╗██╗████████╗
██╔══██╗██║████╗  ██║██║╚══██╔══╝
███████║██║██╔██╗ ██║██║   ██║   
██╔══██║██║██║╚██╗██║██║   ██║   
██║  ██║██║██║ ╚████║██║   ██║   
╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   
</pre>

### Scaffold Production-Ready AI Agent Projects in Seconds

[![PyPI - Version](https://img.shields.io/pypi/v/ai-init?style=for-the-badge&color=blue&logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/ai-init/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Powered by uv](https://img.shields.io/badge/powered%20by-uv-de5b8a?style=for-the-badge&logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*An interactive CLI that bootstraps modular Python projects for AI agents with [`uv`](https://github.com/astral-sh/uv) — frameworks, providers, tests, lint, type-check, and agent rules ready on day one.*

[Quick Start](#quick-start) · [Options](#scaffold-options) · [Features](#features) · [Architecture](#generated-architecture) · [Developing ainit](#developing-ainit) · [Contributing](#contributing) · [License](#license)

</div>

---

## Quick Start

Run without a global install:

```bash
uvx --from ai-init ainit my_project
```

Or install the CLI:

```bash
# Recommended
uv tool install ai-init

# Or
pipx install ai-init

ainit my_project
# equivalent: ainit init my_project
```

Requires Python **3.10+** and [`uv`](https://docs.astral.sh/uv/) on your `PATH` (the scaffold uses `uv init` / `uv add`).

---

## Interactive CLI Experience

`ainit` walks you through the stack, then creates the project:

```text
╭───────────────────────────────────────╮
│  █████╗ ██╗███╗   ██╗██╗████████╗     │
│ ██╔══██╗██║████╗  ██║██║╚══██╔══╝     │
│ ███████║██║██╔██╗ ██║██║   ██║        │
│ ██╔══██║██║██║╚██╗██║██║   ██║        │
│ ██║  ██║██║██║ ╚████║██║   ██║        │
│ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝        │
│ Scaffold AI Agent projects in seconds │
╰───────────────────────────────────────╯
? Framework: LangGraph
? LLM Provider: Gemini
? Storage / Vector DB: None
? Observability: None
? Test runner: Pytest
? Linter/formatter: Ruff
? Type check config: None
? Agent rules: All

🛠️ Creating project in: ./my_project

✨ Project created successfully!

1. cd my_project
2. Fill in the keys in the .env file
3. Run the tests: uv run pytest
4. Try it out: uv run python main.py
```

Defaults: **Pytest**, **Ruff**, type-check **None**, agent rules **All**.

---

## Scaffold Options

| Prompt | Choices |
| --- | --- |
| **Framework** | LangChain, LangGraph, Deep Agents, CrewAI, PydanticAI, Microsoft Agent Framework, LlamaIndex, Google ADK, OpenAI Agents SDK, **None** |
| **LLM Provider** | OpenAI, Anthropic, Groq, DeepSeek, Gemini, Multi-Provider |
| **Storage / Vector DB** | Qdrant, PostgreSQL, Redis, ChromaDB, Neo4j, None |
| **Observability** | LangSmith, Arize, Loguru, OpenTelemetry, None |
| **Test runner** | Pytest *(default)*, unittest |
| **Linter/formatter** | Ruff *(default)*, None |
| **Type check** | None *(default)*, Pyright (Pylance-compatible) |
| **Agent rules** | All *(default)*, AGENTS.md, CLAUDE.md, .cursorrules, None |

### What gets installed

- **Framework / provider**: matching PyPI packages via `uv add` (LangChain adapters only for LangChain / LangGraph / Deep Agents).
- **Storage packages today**: Qdrant → `qdrant-client`; PostgreSQL → `psycopg2-binary`, `pgvector`, `sqlalchemy`; Redis → `redis`. ChromaDB / Neo4j are selectable for project intent; wire-up packages can be extended later.
- **Observability packages today**: LangSmith, Arize Phoenix, Loguru. OpenTelemetry is selectable; package wiring can be extended later.
- **Ruff**: `uv add --dev ruff` + `[tool.ruff]` in `pyproject.toml`.
- **Pyright**: `uv add --dev basedpyright` + `[tool.pyright]` (Pylance reads the same config).
- **Agent rules**: markdown/rules files teaching agents to use `uv` / `uv run` (never `pip`), plus the chosen test/lint commands.
- **`.env`**: provider key placeholders (`OPENAI_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`, etc.).

---

## Features

- **uv-native scaffold** — `uv init` + `uv add` / `uv add --dev`
- **Broad agent framework menu** — including a pure SDK path with **None**
- **Providers** — OpenAI, Anthropic, Groq, DeepSeek, Gemini, Multi-Provider
- **Day-one tooling** — Pytest or unittest smoke tests; optional Ruff and Pyright
- **Agent-ready docs** — optional `AGENTS.md`, `CLAUDE.md`, `.cursorrules`
- **Modular layout** — `src/{agent,tools,models,prompts,storage,utils,api}` + `tests/`

---

## Generated Architecture

```text
my_project/
├── .env                  # Provider key placeholders
├── .gitignore
├── AGENTS.md             # Optional (Cursor)
├── CLAUDE.md             # Optional (Claude Code)
├── .cursorrules          # Optional
├── pyproject.toml        # uv-managed (+ ruff/pyright when selected)
├── main.py               # Entry point
├── src/
│   ├── agent/
│   ├── api/
│   ├── models/llm.py     # Stub LLM factory
│   ├── prompts/
│   ├── storage/
│   ├── tools/
│   └── utils/
└── tests/
    └── test_smoke.py     # Pytest or unittest
```

---

## Post-Setup Workflow

```bash
cd my_project
# edit .env with real API keys
```

**Tests** (depends on what you chose):

```bash
uv run pytest
# or
uv run python -m unittest
```

**Lint / format** (if Ruff was selected):

```bash
uv run ruff check .
uv run ruff format .
```

**Type check** (if Pyright was selected):

```bash
uv run basedpyright
```

**Run**:

```bash
uv run python main.py
```

---

## Developing ainit

This repository (the CLI itself) uses `uv` + Ruff + Pytest. CI runs on every push/PR to `main`.

```bash
git clone https://github.com/mpraes/ainit.git
cd ainit
uv sync --extra dev

uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest
```

Local CLI against your checkout:

```bash
uv run ainit my_project
# or
PYTHONPATH=src python -m ainit.cli my_project
```

Releases: bump `version` in `pyproject.toml`, merge to `main`, then tag `vX.Y.Z` (see `.github/workflows/release.yml`).

---

## Contributing

1. Fork and create a feature branch.
2. Use `uv` for dependencies (`uv add` / `uv sync`) — not `pip`.
3. Keep changes typed and covered by tests where practical.
4. Run `uv run ruff check src tests`, `uv run ruff format src tests`, and `uv run pytest` before opening a PR.
5. Open a Pull Request against `main`.

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE).

Developed with ❤️ by **[@mpraes](https://github.com/mpraes)**.
