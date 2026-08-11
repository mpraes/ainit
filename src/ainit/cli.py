"""ainit CLI entrypoints."""

from __future__ import annotations

import sys

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ainit.choices import ProjectChoices
from ainit.generator import build_project, resolve_test_command
from ainit.ui import print_banner, prompt_choices

cli = typer.Typer(
    name="ainit",
    help="CLI to scaffold AI agent projects with UV",
)
console = Console()

_RESERVED = {
    "init",
    "--help",
    "-h",
    "--install-completion",
    "--show-completion",
}


def _print_success(folder: str, choices: ProjectChoices) -> None:
    cmd = resolve_test_command(choices["test_runner"])
    console.print("[bold green]✨ Project created successfully![/bold green]\n")
    console.print(f"1. [cyan]cd {folder}[/cyan]")
    console.print("2. Fill in the keys in the [yellow].env[/yellow] file")
    console.print(f"3. Run the tests: [cyan]{cmd}[/cyan]")
    console.print("4. Try it out: [cyan]uv run python main.py[/cyan]\n")


def _run_init(folder: str) -> None:
    print_banner()
    choices = prompt_choices()
    console.print(
        f"\n[bold green]🛠️ Creating project in:[/bold green] "
        f"[bold yellow]./{folder}[/bold yellow]\n"
    )
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Installing packages and configuring project...",
            total=None,
        )
        build_project(folder, choices)
    _print_success(folder, choices)


def _safe_run(folder: str) -> None:
    try:
        _run_init(folder)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled.[/yellow]")
        raise typer.Exit(code=130) from None


@cli.callback()
def _root() -> None:
    """CLI to scaffold AI agent projects with UV."""


@cli.command(name="init")
def init(
    folder: str = typer.Argument("my_project", help="Project folder name"),
) -> None:
    """Start the interactive menu to create the project structure."""
    _safe_run(folder)


def app() -> None:
    """Entry point: accepts `ainit <folder>` and `ainit init <folder>`."""
    args = sys.argv[1:]
    if not args:
        sys.argv.append("init")
    elif args[0] not in _RESERVED:
        sys.argv.insert(1, "init")
    cli()


if __name__ == "__main__":
    app()
