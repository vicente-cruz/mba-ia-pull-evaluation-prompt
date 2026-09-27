"""Valida o prompt local, sem credenciais e sem chamadas de API."""

import re
import sys
from pathlib import Path

import pytest
import yaml
from langchain_core.prompts import ChatPromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="module")
def prompt_data():
    document = load_prompts(str(PROJECT_ROOT / "prompts" / "bug_to_user_story_v2.yml"))
    assert isinstance(document, dict), "O YAML deve conter um dicionário."
    assert set(document) == {"bug_to_user_story_v2"}, "Chave principal incorreta."
    data = document["bug_to_user_story_v2"]
    assert isinstance(data, dict), "O conteúdo da v2 deve ser um dicionário."
    return data


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        text = prompt_data.get("system_prompt")
        assert isinstance(text, str) and text.strip(), "system_prompt vazio ou ausente."

    def test_prompt_has_role_definition(self, prompt_data):
        # Examina as instruções, não a persona incidental de um exemplo.
        instructions = prompt_data["system_prompt"].split("EXEMPLOS FEW-SHOT", 1)[0]
        assert re.search(
            r"Você é (?:um|uma)\s+[^\n.]+", instructions, re.IGNORECASE
        ), "Defina explicitamente o papel do modelo."

    def test_prompt_mentions_format(self, prompt_data):
        instructions = prompt_data["system_prompt"].split("EXEMPLOS FEW-SHOT", 1)[0]
        assert "markdown" in instructions.lower()
        assert re.search(r"Como .*eu quero .*para que", instructions, re.IGNORECASE)
        assert "Critérios de Aceitação" in instructions

    def test_prompt_has_few_shot_examples(self, prompt_data):
        text = prompt_data["system_prompt"]
        assert "EXEMPLOS FEW-SHOT" in text
        examples = text.split("EXEMPLOS FEW-SHOT", 1)[1].split("FIM DOS EXEMPLOS", 1)[0]
        pairs = re.findall(
            r"^Entrada:\s*\n(.*?)^Saída:\s*\n(.*?)(?=^\s*### Exemplo|\Z)",
            examples, flags=re.MULTILINE | re.DOTALL,
        )
        assert len(pairs) >= 2, "Few-shot exige múltiplos pares de entrada/saída."
        for input_text, output_text in pairs:
            assert len(input_text.strip()) > 10, "Entrada de exemplo vazia ou insuficiente."
            assert len(output_text.strip()) > 30, "Saída de exemplo vazia ou insuficiente."
            assert "## " in output_text, "A saída do exemplo deve demonstrar Markdown."

    def test_prompt_no_todos(self, prompt_data):
        text = yaml.safe_dump(prompt_data, allow_unicode=True)
        assert not re.search(r"\bTODO\b", text, re.IGNORECASE), "Remova os TODOs."

    def test_minimum_techniques(self, prompt_data):
        techniques = prompt_data.get("techniques_applied")
        assert isinstance(techniques, list)
        assert all(isinstance(item, str) and item.strip() for item in techniques)
        names = {item.strip().lower().replace("_", "-") for item in techniques}
        assert len(names) >= 2, "Use pelo menos duas técnicas distintas."
        assert names.intersection({"few-shot", "few-shot learning", "few-shot-learning"})
        valid, errors = validate_prompt_structure(prompt_data)
        assert valid, "; ".join(errors)

    def test_template_preserves_bug_report(self, prompt_data):
        """Garante compatibilidade com o avaliador e separação system/user."""
        system = prompt_data["system_prompt"]
        user = prompt_data["user_prompt"]
        assert "{bug_report}" not in system
        assert user.count("{bug_report}") == 1
        template = ChatPromptTemplate.from_messages([("system", system), ("human", user)])
        assert set(template.input_variables) == {"bug_report"}
        report = 'O aplicativo exibiu o texto literal {erro} ao salvar.'
        messages = template.format_messages(bug_report=report)
        assert [message.type for message in messages] == ["system", "human"]
        assert messages[0].content == system
        assert report in messages[1].content


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
