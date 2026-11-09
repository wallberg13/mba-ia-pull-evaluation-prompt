"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# Ajuste para o yaml sair montando bonitinho.
import yaml
def str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)
yaml.add_representer(str, str_representer)

load_dotenv()

# Configs
POOR_PROMPT_ID = 'wallbergmorais/bug_to_user_story_v1'
PROMPT_PATH = f"{Path(__file__).parent.parent}/prompts/bug_to_user_story_v2.yml"
REQUIRED_ENV_VARS = ['LANGSMITH_API_KEY', 'USERNAME_LANGSMITH_HUB', 'OPENAI_API_KEY', 'LLM_PROVIDER', 'LLM_MODEL', 'EVAL_MODEL']

# Check .envs
def check_envs():
    print_section_header("Verificando .envs obrigatórias")
    if not check_env_vars(REQUIRED_ENV_VARS):
        print("Erro: Variáveis de ambiente faltando")
        sys.exit(1)
    print("Variáveis de ambiente verificadas com sucesso")

# Get message.
def get_prompt_content(messages, instanceType):
    return next(message for message in messages if isinstance(message, instanceType))

# Format prompt incoming from LangSmith
def format_prompt(prompt):
    print(prompt)
    return {
        "_type": "prompt",
        "name": "bug_to_user_story_v1",
        "description": "Prompt para converter relatos de bugs em User Stories",
        "input_variables": getattr(prompt, "input_variables", []),
        "input_types": getattr(prompt, "input_types", []),
        "template_format": getattr(prompt, "template_format", 'f-string'),
        "system_prompt": get_prompt_content(prompt.messages, SystemMessagePromptTemplate).prompt.template,
        "user_prompt": get_prompt_content(prompt.messages, HumanMessagePromptTemplate).prompt.template,
        "version": "1.0.0",
        "techniques_applied": ["Few-shot", "Chain of Thought"],
    }

# Faço o pull do prompt do LangSmith
def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt(POOR_PROMPT_ID, dangerously_pull_public_prompt=True)
    save_yaml(format_prompt(prompt), PROMPT_PATH)


def main():
    """Função principal"""
    print_section_header("Pulling prompts from LangSmith")
    print(f"Prompt ID: {POOR_PROMPT_ID}")
    print(f"Prompt Path: {PROMPT_PATH}")

    """Check .envs"""
    check_envs()

    """Pull prompts from LangSmith"""
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
