import json
from unittest.mock import Mock
import pytest
from tour_guide.common.tour import Tour
from tour_guide.tour_creation.views import (
    create_tour_view,
    theme_suggestions_view,
)
from django.conf import settings

settings.configure()


@pytest.fixture
def mock_tour_generator(monkeypatch):
    tour_generator = Mock()
    monkeypatch.setattr(
        "tour_guide.tour_creation.views.TourGenerator",
        Mock(return_value=tour_generator),
    )
    return tour_generator


@pytest.fixture
def mock_tour_generation_agent(monkeypatch):
    tour_generation_agent = Mock()
    monkeypatch.setattr(
        "tour_guide.tour_creation.views.tour_generation_agent",
        tour_generation_agent,
    )
    return tour_generation_agent


@pytest.fixture
def mock_request():
    request = Mock()
    request.method = "GET"
    return request


def test_create_tour_view(mock_tour_generator, mock_request):
    expected_tour = Tour(
        title="Test Tour",
        description="A test tour",
        distance_mi=5,
        stops=[],
    )
    mock_tour_generator.create_tour.return_value = expected_tour
    data = {
        "start_location": "New York",
        "distance_mi": 10,
        "theme": "History",
    }
    mock_request.body.decode.return_value = json.dumps(data)
    response = create_tour_view(mock_request)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8"))["tour"]
        == expected_tour.dict()
    )
    mock_tour_generator.create_tour.assert_called_once_with(
        start_location="New York", distance_mi=10, theme="History"
    )


def test_create_tour_view_missing_field(mock_tour_generator, mock_request):
    expected_tour = Tour(
        title="Test Tour",
        description="A test tour",
        distance_mi=5,
        stops=[],
    )
    mock_tour_generator.create_tour.return_value = expected_tour
    data = {
        "start_location": "New York",
        "theme": "History",
    }
    mock_request.body.decode.return_value = json.dumps(data)
    response = create_tour_view(mock_request)
    assert response.status_code == 400


def test_theme_suggestions_view(mock_tour_generation_agent, mock_request):
    expected_theme_suggestions = ["History", "Art", "Culture"]
    mock_tour_generation_agent.get_theme_suggestions.return_value = (
        expected_theme_suggestions
    )
    data = {"start_location": "Paris"}
    mock_request.body.decode.return_value = json.dumps(data)
    response = theme_suggestions_view(mock_request)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8"))["theme_suggestions"]
        == expected_theme_suggestions
    )
    mock_tour_generation_agent.get_theme_suggestions.assert_called_once_with(
        "Paris"
    )


def test_theme_suggestions_view_missing_location(
    mock_tour_generation_agent, mock_request
):
    expected_theme_suggestions = ["History", "Art", "Culture"]
    mock_tour_generation_agent.get_theme_suggestions.return_value = (
        expected_theme_suggestions
    )
    data = {}
    mock_request.body.decode.return_value = json.dumps(data)
    response = theme_suggestions_view(mock_request)
    assert response.status_code == 400
