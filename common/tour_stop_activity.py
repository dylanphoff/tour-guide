from abc import ABC, abstractmethod
from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class TourStopActivityType(Enum):
    TRIVIA = 1
    IMAGE = 2


class RawTourStopActivity(BaseModel):
    type: str = Field("type of tour stop activity")
    content_dict: dict = Field("dict containing the activity's content")


class TourStopActivity(BaseModel, ABC):
    @abstractmethod
    def get_type(self) -> TourStopActivityType:
        pass


class TriviaActivity(TourStopActivity):
    question: str
    answer_options: List[str]
    correct_answer_index: int

    def get_type(self) -> TourStopActivityType:
        return TourStopActivityType.TRIVIA


class ImageActivity(TourStopActivity):
    image_url: str
    description: str

    def get_type(self) -> TourStopActivityType:
        return TourStopActivityType.IMAGE
