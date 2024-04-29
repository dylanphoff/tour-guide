from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from tour_guide.common.tour_stop_activity import (
    RawTourStopActivity,
    TourStopActivity,
)


class TourStop(BaseModel):
    location: str = Field(description="location of this tour stop")
    teaser: str = Field(
        description="short introduction of this stop to be read before it is reached"
    )
    background: str = Field(
        description="background information about this stop"
    )
    key_facts: List[str] = Field(
        description="list of key facts about this stop"
    )
    activities: List[RawTourStopActivity] = Field(
        description="list of activities to complete at this stop"
    )
    executable_activities: List[TourStopActivity] = []
