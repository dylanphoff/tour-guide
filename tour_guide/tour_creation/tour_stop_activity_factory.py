from tour_guide.common.tour_stop_activity import (
    ImageActivity,
    RawTourStopActivity,
    TourStopActivity,
    TourStopActivityType,
    TriviaActivity,
)
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper


class TourStopActivityFactory:
    def create_tour_stop_activity(
        self, raw_tour_stop_activity: RawTourStopActivity
    ) -> TourStopActivity:
        if (
            raw_tour_stop_activity.type
            == TourStopActivityType.TRIVIA.name.lower()
        ):
            return self._generate_triva_activity(
                raw_tour_stop_activity.content_dict
            )
        elif (
            raw_tour_stop_activity.type
            == TourStopActivityType.IMAGE.name.lower()
        ):
            return self._generate_image_activity(
                raw_tour_stop_activity.content_dict
            )
        raise ValueError(
            "No tour stop activity type matching "
            f"{raw_tour_stop_activity.type}"
        )

    def _generate_triva_activity(self, content_dict: dict) -> TriviaActivity:
        return TriviaActivity(
            question=content_dict["question"],
            answer_options=content_dict["answer_options"],
            correct_answer_index=content_dict["correct_answer_index"],
        )

    def _generate_image_activity(self, content_dict: dict) -> ImageActivity:
        prompt = content_dict["prompt"]
        image_url = DallEAPIWrapper().run(prompt)
        return ImageActivity(
            image_url=image_url,
            description=content_dict["description"]
        )
