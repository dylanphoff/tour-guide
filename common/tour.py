from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from common.tour_stop import TourStop


class Tour(BaseModel):
    title: str = Field(description="title of this tour")
    description: str = Field(description="high-level overview of this tour")
    distance_mi: int = Field(description="distance in miles this tour covers")
    stops: List[TourStop] = Field(
        description="list of all stops included in this tour"
    )
    curr_index = 0

    def next_stop(self) -> TourStop:
        if self.completed():
            raise Exception()
        stop = self.stops[self.curr_index]
        self.curr_index += 1
        return stop

    def completed(self) -> bool:
        return len(self.stops) <= self.curr_index


class NullTour(Tour):
    pass
