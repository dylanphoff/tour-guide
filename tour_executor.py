from common.tour import Tour
from tour_stop_activity_executor import TourStopActivityExecutor
from typing import List


class TourExecutor():
    def __init__(self, tour_stop_activity_executor: TourStopActivityExecutor):
        self.tour_stop_activity_executor = tour_stop_activity_executor

    def execute_tour(self, tour: Tour) -> None:
        print(tour.title)
        print(tour.description)
        while not tour.completed():
            stop = tour.next_stop()
            print(stop.teaser + '\n')
            input(f"Walk to {stop.location} and hit Enter when you arrive ")
            print(
                f"""
                Background:\n
                {stop.background}\n
                \n
                Key Facts:\n
                {self._get_key_facts_str(stop.key_facts)}\n
                """
            )
            for activity in stop.executable_activities:
                input("Hit Enter to continue")
                self.tour_stop_activity_executor.execute_activity(activity)
            input("Hit Enter to continue")

    def _get_key_facts_str(self, key_facts: List[str]) -> str:
        return '\n'.join(f'-{key_fact}' for key_fact in key_facts)
