from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from tour_guide.common.tour_stop import TourStop


class Tour(BaseModel):
    title: str = Field(description="title of this tour")
    description: str = Field(description="high-level overview of this tour")
    distance_mi: int = Field(description="distance in miles this tour covers")
    stops: List[TourStop] = Field(
        description="list of all stops included in this tour"
    )


class NullTour(Tour):
    pass
