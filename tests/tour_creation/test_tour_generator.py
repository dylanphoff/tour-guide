from unittest.mock import Mock
import pytest
from common.tour import Tour
from common.tour_stop import TourStop
from common.tour_stop_activity import RawTourStopActivity
from tour_creation.tour_generator import TourGenerator


@pytest.fixture
def mock_agent():
    return Mock()


@pytest.fixture
def mock_tour_stop_activity_factory():
    return Mock()


@pytest.fixture
def tour_generator(mock_agent, mock_tour_stop_activity_factory):
    return TourGenerator(mock_agent, mock_tour_stop_activity_factory)


def test_get_theme_suggestions(mock_agent, tour_generator):
    mock_agent.get_theme_suggestions.return_value = [
        "History",
        "Art",
        "Culture",
    ]
    start_location = "Paris"
    suggestions = tour_generator.get_theme_suggestions(start_location)
    assert suggestions == ["History", "Art", "Culture"]
    mock_agent.get_theme_suggestions.assert_called_once_with(start_location)


def test_generate_tour_success(mock_agent, tour_generator):
    expected_tour = Tour(
        title="Test Tour",
        description="A test tour",
        distance_mi=5,
        stops=[],
    )
    mock_agent.generate_tour.return_value = expected_tour
    start_location = "Paris"
    distance_mi = 5
    theme = "History"
    tour = tour_generator.create_tour(start_location, distance_mi, theme)
    assert tour == expected_tour
    mock_agent.generate_tour.assert_called_once_with(
        start_location=start_location,
        distance_mi=distance_mi,
        approx_stops=10,
        theme=theme,
    )


def test_generate_tour_failure(mock_agent, tour_generator):
    mock_agent.generate_tour.side_effect = Exception("Test Exception")
    start_location = "Paris"
    distance_mi = 12.5
    theme = "History"
    with pytest.raises(Exception):
        tour_generator.create_tour(start_location, distance_mi, theme)
    mock_agent.generate_tour.assert_called_once_with(
        start_location=start_location,
        distance_mi=distance_mi,
        approx_stops=12,
        theme=theme,
    )


def test_fill_executable_activities(
    mock_agent,
    mock_tour_stop_activity_factory,
    tour_generator,
):
    stop_1 = TourStop(
        location="location",
        teaser="teaser",
        background="background",
        key_facts=[],
        activities=[
            RawTourStopActivity(
                type="type",
                content_dict={},
            ),
        ],
        executable_activities=[],
    )
    stop_2 = TourStop(
        location="location",
        teaser="teaser",
        background="background",
        key_facts=[],
        activities=[
            RawTourStopActivity(
                type="type",
                content_dict={},
            ),
            RawTourStopActivity(
                type="type",
                content_dict={},
            ),
        ],
        executable_activities=[],
    )
    partial_tour = Tour(
        title="Test Tour",
        description="A test tour",
        distance_mi=5,
        stops=[stop_1, stop_2],
    )
    mock_agent.generate_tour.return_value = partial_tour
    mock_tour_stop_activity_factory.create_tour_stop_activity.side_effect = [
        Mock(),
        None,
        Mock(),
    ]
    tour = tour_generator.create_tour(
        start_location="Paris",
        distance_mi=5,
        theme="History",
    )
    assert len(tour.stops[0].executable_activities) == 1
    assert len(tour.stops[1].executable_activities) == 1
