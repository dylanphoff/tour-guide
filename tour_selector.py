import logging

from common.tour import NullTour, Tour
from tour_creation.tour_generator import TourGenerator


logger = logging.getLogger(__name__)


class TourSelector:
    def __init__(self, tour_generator: TourGenerator):
        self.tour_generator = tour_generator

    def select_tour(self) -> Tour:
        tour = None
        while tour is None:
            tour = self._create_possible_tour()
            logger.debug("Possible tour created: %s", str(tour))
            if not self._should_select_tour(tour):
                tour = None
        return tour

    def _create_possible_tour(self) -> Tour:
        start_location = input(
            "Where should we start the tour? (\"Exit\" to exit) "
        )
        if start_location.lower() == 'exit':
            return NullTour()
        theme = self._get_theme(start_location)
        distance_mi = self._get_distance_mi()
        approx_stops = self._get_approx_stops(distance_mi)
        return self.tour_generator.create_tour(
            start_location, distance_mi, approx_stops, theme
        )

    def _get_theme(self, start_location: str) -> str:
        theme_suggestions = self.tour_generator.get_theme_suggestions(
            start_location
        )
        if 0 < len(theme_suggestions):
            suggestions_line = f"Suggestions: {','.join(theme_suggestions)}\n"
        else:
            suggestions_line = ""
        theme = input(
            f"""
            What theme would you like this tour to follow?
            {suggestions_line}\
            Enter a theme or \"None\"
            """
        )
        if theme.lower() == 'none':
            return ''
        return theme

    def _get_distance_mi(self) -> float:
        return float(input("How many miles should this tour cover? "))

    def _get_approx_stops(self, distance_mi) -> int:
        if 5 < distance_mi:
            return int(distance_mi * 1)
        return int(distance_mi * 2)

    def _should_select_tour(self, tour: Tour) -> bool:
        if isinstance(tour, NullTour):
            return True
        response = input(
            f"""
            Here's your personalized tour:\n
            Title: {tour.title}\n
            Description: {tour.description}\n
            Distance: {tour.distance_mi}\n
            Stops: {len(tour.stops)}\n

            Would you like to start this tour or create a new one? (start/create)
            """
        ).lower()
        if response not in ('start', 'create'):
            raise ValueError()
        return response == 'start'
