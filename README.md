# 🚀 ainit

> The fastest way to scaffold ready AI Agent projects.

`ainit` is an interactive CLI tool that bootstraps modular Python projects tailored for AI Agents using **`uv`**, pre-configured for modern LLM frameworks, vector stores, and observability tooling.

## 📦 Quick Start

Run directly with `uvx` without installing:

```bash
uvx ainit init my_project
```

Or install globally via `pip`:

```bash
pip install ainit
ainit my_project
```

## ✨ Features

- **⚡ Blazing Fast Setup**: Uses [`uv`](https://github.com/astral-sh/uv) under the hood.
- **🤖 Framework Choice**: LangGraph, CrewAI, PydanticAI, AutoGen, or Custom SDKs.
- **⚡ LLM Providers**: OpenAI, Anthropic, Groq, DeepSeek, and Multi-Provider.
- **🗄️ Storage & Vector DBs**: Qdrant, PGVector, Redis, ChromaDB, Neo4j.
- **📊 Observability**: LangSmith, Phoenix, Loguru, OpenTelemetry.
- **🧪 Built-in Smoke Tests**: Included `pytest` suite ready out of the box.

## 📄 License

MIT © mpraes