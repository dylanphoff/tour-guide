from tour_guide.common.tour_stop_activity import (
    TriviaActivity,
    ImageActivity,
    TourStopActivityType,
)


def test_trivia_activity():
    activity = TriviaActivity(
        question="What is the capital of France?",
        answer_options=["London", "Paris", "Berlin", "Rome"],
        correct_answer_index=1,
    )
    assert activity.get_type() == TourStopActivityType.TRIVIA
    assert activity.question == "What is the capital of France?"
    assert activity.answer_options == ["London", "Paris", "Berlin", "Rome"]
    assert activity.correct_answer_index == 1


def test_image_activity():
    activity = ImageActivity(
        image_url="https://example.com/image.jpg",
        description="An image of the Eiffel Tower",
    )
    assert activity.get_type() == TourStopActivityType.IMAGE
    assert activity.image_url == "https://example.com/image.jpg"
    assert activity.description == "An image of the Eiffel Tower"
