"""Valida e publica o prompt v2 no LangSmith Prompt Hub."""

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

from utils import (
    check_env_vars,
    load_yaml,
    print_section_header,
    validate_prompt_structure,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_NAME = "bug_to_user_story_v2"
PROMPT_FILE = PROJECT_ROOT / "prompts" / f"{PROMPT_NAME}.yml"
load_dotenv(PROJECT_ROOT / ".env")


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """Verifica o YAML e sua compatibilidade com a entrada do avaliador."""
    errors = []
    if not isinstance(prompt_data, dict):
        return False, ["O conteúdo do prompt deve ser um dicionário."]

    for field in ("description", "system_prompt", "user_prompt", "version"):
        value = prompt_data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Campo obrigatório vazio ou inválido: {field}")
    techniques = prompt_data.get("techniques_applied")
    if not isinstance(techniques, list) or not all(
        isinstance(item, str) and item.strip() for item in techniques
    ):
        errors.append("techniques_applied deve ser uma lista de nomes de técnicas.")
    tags = prompt_data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append("tags deve ser uma lista de textos.")
    if errors:
        return False, errors

    _, structure_errors = validate_prompt_structure(prompt_data)
    errors.extend(structure_errors)
    normalized = {item.strip().lower().replace("_", "-") for item in techniques}
    if len(normalized) < 2:
        errors.append("Informe pelo menos duas técnicas distintas.")
    if not normalized.intersection({"few-shot", "few-shot learning", "few-shot-learning"}):
        errors.append("Few-shot é obrigatório nos metadados.")
    if prompt_data["version"] != "v2":
        errors.append("Este script publica somente a versão v2.")
    system = prompt_data["system_prompt"]
    user = prompt_data["user_prompt"]
    if re.search(r"\bTODO\b", str(prompt_data), re.IGNORECASE):
        errors.append("O prompt ainda contém TODOs.")
    if len(re.findall(r"(?mi)^\s*Entrada:\s*$", system)) < 2 or len(
        re.findall(r"(?mi)^\s*Saída:\s*$", system)
    ) < 2:
        errors.append("Inclua pelo menos dois exemplos com marcadores Entrada: e Saída:.")

    try:
        template = ChatPromptTemplate.from_messages([("system", system), ("human", user)])
        if set(template.input_variables) != {"bug_report"}:
            errors.append("A única variável de entrada deve ser bug_report.")
        if "{bug_report}" in system or user.count("{bug_report}") != 1:
            errors.append("Coloque {bug_report} apenas uma vez, no user_prompt.")
        template.format_messages(bug_report="Relato usado somente para validar o template.")
    except (ValueError, KeyError, TypeError) as error:
        errors.append(f"Template inválido: {error}")
    return not errors, errors


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """Publica uma nova revisão pública da v2; retorna True em caso de sucesso."""
    valid, errors = validate_prompt(prompt_data)
    if not valid:
        for error in errors:
            print(f"Erro de validação: {error}")
        return False
    if prompt_name != PROMPT_NAME:
        print(f"Nome inesperado: este script publica apenas {PROMPT_NAME}.")
        return False
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return False

    username = os.environ["USERNAME_LANGSMITH_HUB"].strip()
    if not username or any(char.isspace() for char in username) or "/" in username or ":" in username:
        # Verificação completa de disponibilidade do handle pertence ao LangSmith.
        print("Informe apenas seu handle em USERNAME_LANGSMITH_HUB, sem URL ou nome do prompt.")
        return False

    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"]),
        ])
        techniques = prompt_data["techniques_applied"]
        revision = str(prompt_data.get("revision", "v2"))
        prompt.metadata = {
            "version": "v2",
            "revision": revision,
            "techniques_applied": techniques,
        }
        tags = list(dict.fromkeys(prompt_data.get("tags", []) + techniques + ["v2"]))
        description = (
            f"{prompt_data['description']} Técnicas: {', '.join(techniques)}."
        )
        client = Client()
        identifier = f"{username}/{prompt_name}"
        print(f"Publicando prompt público: {identifier}")
        url = client.push_prompt(
            identifier,
            object=prompt,
            is_public=True,
            description=description,
            tags=tags,
            commit_description=f"{revision}: {', '.join(techniques)}",
        )
        print(f"Prompt publicado: {url}")
        print("Após conferir a publicação e configurar os modelos, execute python src/evaluate.py")
        return True
    except Exception as error:
        detail = str(error)
        key = os.getenv("LANGSMITH_API_KEY", "")
        if key:
            detail = detail.replace(key, "[CHAVE OCULTA]")
        print(f"Falha no push ({type(error).__name__}): {detail}")
        print("Confira a conexão, a chave, as permissões e o handle público do Hub.")
        return False


def main():
    """Carrega o YAML local; retorna 0 no sucesso ou 1 na falha."""
    print_section_header("Push do prompt otimizado para o LangSmith")
    document = load_yaml(str(PROMPT_FILE))
    if not isinstance(document, dict) or set(document) != {PROMPT_NAME}:
        print(f"O YAML precisa conter a chave principal {PROMPT_NAME}.")
        return 1
    return 0 if push_prompt_to_langsmith(PROMPT_NAME, document[PROMPT_NAME]) else 1


if __name__ == "__main__":
    sys.exit(main())
