import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from ainit.ui import print_banner, prompt_choices
from ainit.generator import build_project

app = typer.Typer(name="ainit", help="CLI para criar projetos de agentes com UV")
console = Console()

@app.command()
def init(
    folder: str = typer.Argument("meu_projeto", help="Nome da pasta do projeto"),
):
    """Inicia o menu interativo para criar a estrutura do projeto."""
    print_banner()
    
    choices = prompt_choices()

    console.print(f"\n[bold green]🛠️ Criando o projeto em:[/bold green] [bold yellow]./{folder}[/bold yellow]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Instalando pacotes e configurando projeto...", total=None)
        build_project(folder, choices)

    console.print("[bold green]✨ Projeto criado com sucesso![/bold green]\n")
    console.print(f"1. [cyan]cd {folder}[/cyan]")
    console.print("2. Preencha as chaves no arquivo [yellow].env[/yellow]")
    console.print("3. Execute os testes: [cyan]uv run pytest[/cyan]")
    console.print("4. Teste a execução: [cyan]uv run python main.py[/cyan]\n")

if __name__ == "__main__":
    app()