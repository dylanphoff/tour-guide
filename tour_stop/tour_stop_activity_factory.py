from tour_stop.tour_stop_activity import (
    RawTourStopActivity,
    TourStopActivity,
    TourStopActivityType,
    TriviaActivity,
)


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
