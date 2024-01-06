import logging
from typing import List

from tour import Tour
from tour_generation_assistant import TourGenerationAssistant
from tour_stop.tour_stop_activity import RawTourStopActivity, TourStopActivity
from tour_stop.tour_stop_activity_factory import TourStopActivityFactory


logger = logging.getLogger(__name__)


class TourGenerator:
    def __init__(
        self,
        assistant: TourGenerationAssistant,
        tour_stop_activity_factory: TourStopActivityFactory,
    ):
        self.assistant = assistant
        self.tour_stop_activity_factory = tour_stop_activity_factory

    def get_theme_suggestions(self, start_location: str) -> List[str]:
        return self.assistant.get_theme_suggestions(start_location)

    def create_tour(
        self,
        start_location: str,
        distance_mi: float,
        approx_stops: int,
        theme: str,
    ) -> Tour:
        tour = self.assistant.generate_tour(
            start_location=start_location,
            distance_mi=distance_mi,
            approx_stops=approx_stops,
            theme=theme,
        )
        self._fill_executable_activities(tour)
        return tour

    def _fill_executable_activities(self, tour: Tour) -> None:
        for tour_stop in tour.stops:
            for raw_tour_stop_activity in tour_stop.activities:
                tour_stop_activity = self._create_tour_stop_activity(
                    raw_tour_stop_activity
                )
                if tour_stop_activity is not None:
                    tour_stop.executable_activities.append(tour_stop_activity)

    def _create_tour_stop_activity(
        self, raw_tour_stop_activity: RawTourStopActivity
    ) -> TourStopActivity:
        try:
            return self.tour_stop_activity_factory.create_tour_stop_activity(
                raw_tour_stop_activity
            )
        except Exception:
            logger.error(
                "Failed to generate executable tour stop activity for %s",
                str(raw_tour_stop_activity),
            )
            return None
