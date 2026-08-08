import os
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def build_project(folder_name: str, config: dict):
    project_path = Path(folder_name).resolve()
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Lista de subpastas do src
    subdirs = ["agent", "tools", "models", "prompts", "storage", "utils", "api"]
    for sd in subdirs:
        (project_path / "src" / sd).mkdir(parents=True, exist_ok=True)
        (project_path / "src" / sd / "__init__.py").touch()
    
    (project_path / "tests").mkdir(exist_ok=True)
    (project_path / "tests" / "__init__.py").touch()

    # Mapeamento de pacotes
    pkgs = ["pydantic", "pydantic-settings", "python-dotenv", "pytest", "pytest-asyncio"]

    if "LangGraph" in config["framework"]:
        pkgs.extend(["langgraph", "langchain-core"])
    elif "CrewAI" in config["framework"]:
        pkgs.append("crewai")
    elif "PydanticAI" in config["framework"]:
        pkgs.append("pydantic-ai")
    elif "AutoGen" in config["framework"]:
        pkgs.extend(["autogen-agentchat", "autogen-ext"])

    if "OpenAI" in config["provider"]:
        pkgs.extend(["openai", "langchain-openai"])
    elif "Anthropic" in config["provider"]:
        pkgs.extend(["anthropic", "langchain-anthropic"])
    elif "Groq" in config["provider"]:
        pkgs.extend(["groq", "langchain-groq"])
    elif "DeepSeek" in config["provider"]:
        pkgs.append("openai")

    if "Qdrant" in config["storage"]:
        pkgs.append("qdrant-client")
    elif "PostgreSQL" in config["storage"]:
        pkgs.extend(["psycopg2-binary", "pgvector", "sqlalchemy"])
    elif "Redis" in config["storage"]:
        pkgs.append("redis")

    if "LangSmith" in config["logging"]:
        pkgs.append("langsmith")
    elif "Arize" in config["logging"]:
        pkgs.append("arize-phoenix")
    elif "Loguru" in config["logging"]:
        pkgs.append("loguru")

    # Executa uv init e adiciona as dependências
    subprocess.run(["uv", "init"], cwd=project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["uv", "add"] + pkgs, cwd=project_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cria .env inicial
    with open(project_path / ".env", "w", encoding="utf-8") as f:
        f.write("# API Keys e Configurações geradas via ainit\n")
        if "OpenAI" in config["provider"]:
            f.write("OPENAI_API_KEY=your_key_here\n")
        elif "Anthropic" in config["provider"]:
            f.write("ANTHROPIC_API_KEY=your_key_here\n")
        elif "Groq" in config["provider"]:
            f.write("GROQ_API_KEY=your_key_here\n")
        elif "DeepSeek" in config["provider"]:
            f.write("DEEPSEEK_API_KEY=your_key_here\n")

    # Cria módulo base de LLM
    with open(project_path / "src" / "models" / "llm.py", "w", encoding="utf-8") as f:
        f.write('''import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Retorna o cliente LLM inicializado."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Chave de API não configurada no arquivo .env")
    return {"status": "configured", "api_key_present": True}
''')

    # Cria main.py
    with open(project_path / "main.py", "w", encoding="utf-8") as f:
        f.write('''from src.models.llm import get_llm

def main():
    print("🤖 Projeto de Agente inicializado com sucesso!")
    client = get_llm()
    print("Status do Modelo:", client)

if __name__ == "__main__":
    main()
''')

    # Cria Smoke Test em tests/test_smoke.py
    with open(project_path / "tests" / "test_smoke.py", "w", encoding="utf-8") as f:
        f.write('''import os

def test_env_file_exists():
    assert os.path.exists(".env")

def test_llm_module_import():
    from src.models.llm import get_llm
    assert callable(get_llm)
''')