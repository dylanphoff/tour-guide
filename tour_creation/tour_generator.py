import logging
from typing import List

from common.tour import Tour
from agent.tour_generation_agent import TourGenerationAgent
from common.tour_stop_activity import RawTourStopActivity, TourStopActivity
from tour_creation.tour_stop_activity_factory import TourStopActivityFactory


logger = logging.getLogger(__name__)


class TourGenerator:
    def __init__(
        self,
        agent: TourGenerationAgent,
        tour_stop_activity_factory: TourStopActivityFactory,
    ) -> None:
        self.agent = agent
        self.tour_stop_activity_factory = tour_stop_activity_factory

    def get_theme_suggestions(self, start_location: str) -> List[str]:
        return self.agent.get_theme_suggestions(start_location)

    def create_tour(
        self,
        start_location: str,
        distance_mi: float,
        theme: str,
    ) -> Tour:
        approx_stops = self._get_approx_stops(distance_mi)
        tour = self._generate_tour(
            start_location=start_location,
            distance_mi=distance_mi,
            approx_stops=approx_stops,
            theme=theme,
        )
        self._fill_executable_activities(tour)
        return tour

    def _generate_tour(
        self,
        start_location: str,
        distance_mi: float,
        approx_stops: int,
        theme: str,
    ) -> Tour:
        try:
            return self.agent.generate_tour(
                start_location=start_location,
                distance_mi=distance_mi,
                approx_stops=approx_stops,
                theme=theme,
            )
        except Exception:
            logger.error(
                "Failed to generate tour with start_location: %s, "
                "distance_mi: %d, approx_stops: %d, theme: %s",
                start_location,
                distance_mi,
                approx_stops,
                theme,
            )
            raise

    def _get_approx_stops(self, distance_mi: float) -> int:
        if 5 < distance_mi:
            return int(distance_mi * 1)
        return int(distance_mi * 2)

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
                "Failed to create executable tour stop activity for %s",
                str(raw_tour_stop_activity),
            )
            return None
