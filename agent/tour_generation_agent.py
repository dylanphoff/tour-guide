from typing import List
import logging
from langchain.llms import OpenAI
from agent.theme_suggestions_prompt import ThemeSuggestionsPrompt
from agent.tour_generation_prompt import TourGenerationPrompt

from common.tour import Tour


logger = logging.getLogger(__name__)


class TourGenerationAgent:
    def __init__(self):
        self.model = OpenAI(
            model_name="gpt-3.5-turbo-instruct", max_tokens=2056
        )

    def generate_tour(
        self,
        start_location: str,
        distance_mi: float,
        approx_stops: int,
        theme: str,
    ) -> Tour:
        prompt = TourGenerationPrompt(
            start_location=start_location,
            distance_mi=distance_mi,
            approx_stops=approx_stops,
            theme=theme,
        )
        prompt_text = prompt.get_prompt_text()
        logging.debug("Tour generation model input: %s", prompt_text)
        model_output = self.model(prompt_text)
        logging.debug("Tour generation model output: %s", model_output)
        return prompt.parse_model_output(model_output)

    def get_theme_suggestions(self, start_location) -> List[str]:
        prompt = ThemeSuggestionsPrompt(start_location=start_location)
        prompt_text = prompt.get_prompt_text()
        logging.debug("Theme suggestion model input: %s", prompt_text)
        model_output = self.model(prompt_text)
        logging.debug("Theme suggestions model output: %s", model_output)
        return prompt.parse_model_output(model_output)
