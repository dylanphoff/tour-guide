import logging
from agent.tour_generation_agent import TourGenerationAgent

from common.tour import NullTour
from tour_creation.tour_generator import TourGenerator
from tour_selector import TourSelector
from tour_stop_activity_executor import TourStopActivityExecutor
from tour_creation.tour_stop_activity_factory import TourStopActivityFactory
from tour_executor import TourExecutor


logger = logging.getLogger(__name__)


class TourGuide():
    def __init__(self):
        agent = TourGenerationAgent()
        tour_stop_activity_factory = TourStopActivityFactory()
        tour_generator = TourGenerator(agent, tour_stop_activity_factory)
        self.tour_selector = TourSelector(tour_generator)
        tour_stop_activity_executor = TourStopActivityExecutor()
        self.tour_executor = TourExecutor(tour_stop_activity_executor)

    def run(self):
        try:
            running = True
            while running:
                tour = self.tour_selector.select_tour()
                if isinstance(tour, NullTour):
                    running = False
                else:
                    self.tour_executor.execute_tour(tour)
        except Exception as e:
            logger.exception("Fatal exception occurred", exc_info=e)
