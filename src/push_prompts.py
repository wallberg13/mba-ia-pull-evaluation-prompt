"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_PATH = f"{Path(__file__).parent.parent}/prompts/bug_to_user_story_v2.yml"
REQUIRED_ENV_VARS = ['LANGSMITH_API_KEY', 'USERNAME_LANGSMITH_HUB', 'OPENAI_API_KEY', 'LLM_PROVIDER', 'LLM_MODEL', 'EVAL_MODEL']

# Check .envs
def check_envs():
    print_section_header("Verificando .envs obrigatórias")
    if not check_env_vars(REQUIRED_ENV_VARS):
        print("Erro: Variáveis de ambiente faltando")
        sys.exit(1)
    print("Variáveis de ambiente verificadas com sucesso")

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    ...


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """


def main():
    """Função principal"""
    print_section_header("Pushing prompts to LangSmith")

    """Check .envs"""
    check_envs()

    """Push prompts to LangSmith"""
    prompt_data = load_yaml(PROMPT_PATH)
    print(prompt_data)
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("user", prompt_data["user_prompt"]),
    ])
    client = Client()
    url = client.push_prompt(
        "wallbergmorais/bug_to_user_story_v2",
        object=prompt,
        is_public=True,
        description="Prompt para converter relatos de bugs em User Stories",
        tags=["v1.0.0", "model: gpt-4o-mini"],
    )
    print(url)


if __name__ == "__main__":
    sys.exit(main())
