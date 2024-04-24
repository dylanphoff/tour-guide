import pytest
from agent.theme_suggestions_prompt import ThemeSuggestionsPrompt
from unittest.mock import Mock


@pytest.fixture
def prompt():
    return ThemeSuggestionsPrompt("New York")


def test_get_prompt_text(prompt):
    expected_prompt_text = """
You are creating an itinerary for a tour with a starting location of New York.

Suggest 3 to 5 possible interesting themes for the tour taking into account 
the starting location and the area around it which will be covered in the tour.

Your output should be a valid JSON list of strings and nothing else 
(e.g. ["theme 1", "theme 2", "theme 3"])
"""
    assert prompt.get_prompt_text() == expected_prompt_text


def test_parse_model_output(monkeypatch, prompt):
    monkeypatch.setattr(
        "json.loads", Mock(return_value=["theme 1", "theme 2", "theme 3"])
    )
    assert prompt.parse_model_output("model output") == [
        "theme 1",
        "theme 2",
        "theme 3",
    ]
