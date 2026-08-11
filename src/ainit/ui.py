"""Interactive prompts for scaffold options."""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ainit.choices import (
    AGENT_RULE_OPTIONS,
    FRAMEWORKS,
    LINTERS,
    OBSERVABILITY_OPTIONS,
    PROVIDERS,
    STORAGE_OPTIONS,
    TEST_RUNNERS,
    TYPE_CHECKS,
    ProjectChoices,
)

console = Console()

BANNER = r"""
 █████╗ ██╗███╗   ██╗██╗████████╗
██╔══██╗██║████╗  ██║██║╚══██╔══╝
███████║██║██╔██╗ ██║██║   ██║   
██╔══██║██║██║╚██╗██║██║   ██║   
██║  ██║██║██║ ╚████║██║   ██║   
╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   
"""


def print_banner() -> None:
    """Print the ainit ASCII banner.

    Example:
        print_banner()
    """
    logo = Text(BANNER.strip("\n"), style="bold cyan")
    subtitle = Text("Scaffold AI Agent projects in seconds", style="dim")
    console.print(Panel.fit(Text.assemble(logo, "\n", subtitle), border_style="cyan"))


def _select(message: str, choices: list[str], default: str | None = None) -> str:
    kwargs: dict[str, object] = {"message": message, "choices": choices}
    if default is not None:
        kwargs["default"] = default
    value = questionary.select(**kwargs).ask()
    if value is None:
        raise KeyboardInterrupt
    return str(value)


def prompt_choices() -> ProjectChoices:
    """Collect scaffold options from the interactive menu.

    Example:
        choices = prompt_choices()
        build_project("my_app", choices)
    """
    return {
        "framework": _select("Framework:", FRAMEWORKS),
        "provider": _select("LLM Provider:", PROVIDERS),
        "storage": _select("Storage / Vector DB:", STORAGE_OPTIONS),
        "logging": _select("Observability:", OBSERVABILITY_OPTIONS),
        "test_runner": _select("Test runner:", TEST_RUNNERS, default="Pytest"),
        "linter": _select("Linter/formatter:", LINTERS, default="Ruff"),
        "type_check": _select("Type check config:", TYPE_CHECKS, default="None"),
        "agent_rules": _select("Agent rules:", AGENT_RULE_OPTIONS, default="All"),
    }
