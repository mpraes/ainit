import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


BANNER = r"""
__ _   _ _ __   (*) | |_   _| | |_
 / _` | | | '_ \  | | | __| | | | __|
| (_| | | | | | | | | | |_  | | | |_
 \__,_| |_|_| |_| |_|  \__| |_|  \__|
"""


def print_banner() -> None:
    logo = Text(BANNER.strip("\n"), style="bold cyan")
    subtitle = Text("Scaffold AI Agent projects in seconds", style="dim")
    console.print(Panel.fit(Text.assemble(logo, "\n", subtitle), border_style="cyan"))


def prompt_choices() -> dict:
    framework = questionary.select(
        "Framework:",
        choices=["LangGraph", "CrewAI", "PydanticAI", "AutoGen", "Custom"],
    ).ask()

    provider = questionary.select(
        "LLM Provider:",
        choices=["OpenAI", "Anthropic", "Groq", "DeepSeek", "Multi-Provider"],
    ).ask()

    storage = questionary.select(
        "Storage / Vector DB:",
        choices=["Qdrant", "PostgreSQL", "Redis", "ChromaDB", "Neo4j", "None"],
    ).ask()

    logging = questionary.select(
        "Observability:",
        choices=["LangSmith", "Arize", "Loguru", "OpenTelemetry", "None"],
    ).ask()

    if None in (framework, provider, storage, logging):
        raise KeyboardInterrupt

    return {
        "framework": framework,
        "provider": provider,
        "storage": storage,
        "logging": logging,
    }
