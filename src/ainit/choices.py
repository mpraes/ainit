from typing import TypedDict


class ProjectChoices(TypedDict):
    framework: str
    provider: str
    storage: str
    logging: str
    test_runner: str
    linter: str
    type_check: str
    agent_rules: str


FRAMEWORKS: list[str] = [
    "LangChain",
    "LangGraph",
    "Deep Agents",
    "CrewAI",
    "PydanticAI",
    "Microsoft Agent Framework",
    "LlamaIndex",
    "Google ADK",
    "OpenAI Agents SDK",
    "None",
]

PROVIDERS: list[str] = [
    "OpenAI",
    "Anthropic",
    "Groq",
    "DeepSeek",
    "Gemini",
    "Multi-Provider",
]

STORAGE_OPTIONS: list[str] = [
    "Qdrant",
    "PostgreSQL",
    "Redis",
    "ChromaDB",
    "Neo4j",
    "None",
]

OBSERVABILITY_OPTIONS: list[str] = [
    "LangSmith",
    "Arize",
    "Loguru",
    "OpenTelemetry",
    "None",
]

TEST_RUNNERS: list[str] = ["Pytest", "unittest"]
LINTERS: list[str] = ["Ruff", "None"]
TYPE_CHECKS: list[str] = ["None", "Pyright (Pylance-compatible)"]
AGENT_RULE_OPTIONS: list[str] = [
    "All",
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    "None",
]
