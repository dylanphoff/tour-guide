from unittest.mock import Mock
import pytest
from agent.tour_generation_agent import TourGenerationAgent
from common.tour import Tour


@pytest.fixture
def mock_model():
    model = Mock()
    model.return_value = "Mocked model output"
    return model


def test_generate_tour(monkeypatch, mock_model):
    expected_tour = Tour(
        title="Test Tour",
        description="A test tour",
        distance_mi=5,
        stops=[],
    )
    mock_parse_model_output = Mock(return_value=expected_tour)
    monkeypatch.setattr(
        "agent.tour_generation_agent.TourGenerationPrompt.parse_model_output",
        mock_parse_model_output,
    )
    agent = TourGenerationAgent()
    agent.model = mock_model
    tour = agent.generate_tour(
        start_location="New York",
        distance_mi=100,
        approx_stops=5,
        theme="Architecture",
    )
    assert tour == expected_tour
    mock_parse_model_output.assert_called_once_with("Mocked model output")


def test_get_theme_suggestions(monkeypatch, mock_model):
    expected_theme_suggestions = ["theme 1", "theme 2", "theme 3"]
    mock_parse_model_output = Mock(return_value=expected_theme_suggestions)
    monkeypatch.setattr(
        "agent.tour_generation_agent.ThemeSuggestionsPrompt.parse_model_output",
        mock_parse_model_output,
    )
    agent = TourGenerationAgent()
    agent.model = mock_model
    theme_suggestions = agent.get_theme_suggestions(start_location="New York")
    assert theme_suggestions == expected_theme_suggestions
    mock_parse_model_output.assert_called_once_with("Mocked model output")
