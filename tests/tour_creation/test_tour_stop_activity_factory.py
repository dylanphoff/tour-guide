from unittest.mock import Mock
import pytest
from common.tour_stop_activity import (
    TriviaActivity,
    ImageActivity,
    RawTourStopActivity,
)
from tour_creation.tour_stop_activity_factory import TourStopActivityFactory


@pytest.fixture
def mock_dalle_api_wrapper(monkeypatch):
    wrapper = Mock()
    wrapper.return_value.run.return_value = "https://example.com/image.jpg"
    monkeypatch.setattr(
        "tour_creation.tour_stop_activity_factory.DallEAPIWrapper",
        wrapper,
    )
    return wrapper


def test_create_trivia_activity():
    tour_stop_activity_factory = TourStopActivityFactory()
    raw_activity = RawTourStopActivity(
        type="trivia",
        content_dict={
            "question": "What is the capital of France?",
            "answer_options": ["London", "Paris", "Berlin", "Rome"],
            "correct_answer_index": 1,
        },
    )
    activity = tour_stop_activity_factory.create_tour_stop_activity(
        raw_activity
    )
    assert isinstance(activity, TriviaActivity)
    assert activity.question == "What is the capital of France?"
    assert activity.answer_options == ["London", "Paris", "Berlin", "Rome"]
    assert activity.correct_answer_index == 1


def test_create_image_activity(mock_dalle_api_wrapper):
    tour_stop_activity_factory = TourStopActivityFactory()
    raw_activity = RawTourStopActivity(
        type="image",
        content_dict={
            "prompt": "Generate an image of the Eiffel Tower",
            "description": "An image of the Eiffel Tower",
        },
    )
    activity = tour_stop_activity_factory.create_tour_stop_activity(
        raw_activity
    )
    assert isinstance(activity, ImageActivity)
    assert activity.image_url == "https://example.com/image.jpg"
    assert activity.description == "An image of the Eiffel Tower"


def test_create_unknown_activity():
    tour_stop_activity_factory = TourStopActivityFactory()
    raw_activity = RawTourStopActivity(type="invalid", content_dict={})
    with pytest.raises(ValueError):
        tour_stop_activity_factory.create_tour_stop_activity(raw_activity)
