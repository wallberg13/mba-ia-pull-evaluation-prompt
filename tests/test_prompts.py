"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture
def prompt():
    return load_prompts(PROMPT_PATH)


@pytest.fixture
def prompt_text(prompt):
    return f"{prompt.get('system_prompt', '')}\n{prompt.get('user_prompt', '')}"


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip()

        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, errors

    def test_prompt_has_role_definition(self, prompt_text):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert "Você é" in prompt_text

    def test_prompt_mentions_format(self, prompt_text):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = prompt_text.lower()
        assert "user story" in text
        assert "como" in text and "quero" in text and "para" in text
        assert "given-when-then" in text or "critérios de aceite" in text

    def test_prompt_has_few_shot_examples(self, prompt, prompt_text):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        assert "Relato:" in prompt_text
        assert "Saída:" in prompt_text
        assert "Few-shot" in prompt.get("techniques_applied", [])

    def test_prompt_no_todos(self, prompt_text):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        assert "[TODO]" not in prompt_text
        assert "TODO" not in prompt_text

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied", [])
        assert isinstance(techniques, list)
        assert len(techniques) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
