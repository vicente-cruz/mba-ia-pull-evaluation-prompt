"""Baixa o prompt semente do LangSmith e salva sua versao v1 em YAML."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langsmith import Client

from utils import check_env_vars, load_yaml, print_section_header, save_yaml


# O arquivo deve ficar em src/pull_prompts.py no projeto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_NAME = "bug_to_user_story_v1"
PROMPT_ID = f"leonanluppi/{PROMPT_NAME}"
OUTPUT_FILE = PROJECT_ROOT / "prompts" / f"{PROMPT_NAME}.yml"

load_dotenv(PROJECT_ROOT / ".env")


def pull_prompts_from_langsmith():
    """Retorna True somente quando o prompt remoto foi salvo com sucesso."""
    # Preserva os metadados que ja vieram no YAML do desafio.
    # Um arquivo local invalido interrompe o processo antes de ser sobrescrito.
    if OUTPUT_FILE.exists():
        document = load_yaml(str(OUTPUT_FILE))
        if not isinstance(document, dict):
            raise ValueError("O YAML local precisa conter um dicionario.")
        if not isinstance(document.get(PROMPT_NAME), dict):
            raise ValueError(f"Chave ausente ou invalida no YAML: {PROMPT_NAME}")
        prompt_data = dict(document[PROMPT_NAME])
    else:
        document = {}
        prompt_data = {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }

    print(f"Baixando: {PROMPT_ID}")
    client = Client()
    # Autorizacao explicita para o prompt publico indicado no desafio.
    # Nao inclui um modelo: esta etapa nao gera respostas com LLM.
    prompt = client.pull_prompt(
        PROMPT_ID,
        include_model=False,
        dangerously_pull_public_prompt=True,
    )

    # O YAML do projeto representa uma mensagem system seguida de uma human.
    # Se o Hub mudar de estrutura, paramos em vez de descartar mensagens.
    if not isinstance(prompt, ChatPromptTemplate):
        raise ValueError("O Hub nao retornou um ChatPromptTemplate.")
    if len(prompt.messages) != 2:
        raise ValueError("Esperadas exatamente duas mensagens: system e human.")

    system_message, user_message = prompt.messages
    if not isinstance(system_message, SystemMessagePromptTemplate):
        raise ValueError("A primeira mensagem precisa ser do tipo system.")
    if not isinstance(user_message, HumanMessagePromptTemplate):
        raise ValueError("A segunda mensagem precisa ser do tipo human.")

    for field, message in (
        ("system_prompt", system_message),
        ("user_prompt", user_message),
    ):
        template = message.prompt
        if getattr(template, "template_format", None) != "f-string":
            raise ValueError(f"Formato de template inesperado em {field}.")
        if getattr(template, "partial_variables", {}):
            raise ValueError(f"Variaveis parciais nao suportadas em {field}.")
        text = template.template
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Texto vazio ou invalido em {field}.")
        # Preserva {bug_report}; nao preenche nem otimiza a versao inicial.
        prompt_data[field] = text

    if prompt.partial_variables:
        raise ValueError("O prompt remoto contem variaveis parciais nao suportadas.")

    document[PROMPT_NAME] = prompt_data
    if not save_yaml(document, str(OUTPUT_FILE)):
        return False

    print(f"Prompt salvo em: {OUTPUT_FILE}")
    print(f"Variaveis de entrada: {', '.join(prompt.input_variables)}")
    return True


def main():
    """Retorna 0 em caso de sucesso ou 1 em caso de falha."""
    print_section_header("Pull do prompt inicial do LangSmith")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    try:
        return 0 if pull_prompts_from_langsmith() else 1
    except Exception as error:
        # Evita exibir a chave caso ela apareca em alguma mensagem de erro.
        detail = str(error)
        api_key = os.getenv("LANGSMITH_API_KEY", "")
        if api_key:
            detail = detail.replace(api_key, "[CHAVE OCULTA]")
        print(f"Falha no pull ({type(error).__name__}): {detail}")
        print("Confira a conexao, as credenciais e as versoes das dependencias.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
