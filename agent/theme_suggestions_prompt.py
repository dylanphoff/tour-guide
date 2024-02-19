import json
from typing import List
from langchain.prompts import PromptTemplate

_PROMPT_TEMPLATE_TEXT = """
You are creating an itinerary for a tour with a starting location of {start_location}.

Suggest 3 to 5 possible interesting themes for the tour taking into account 
the starting location and the area around it which will be covered in the tour.

Your output should be a valid JSON list of strings and nothing else 
(e.g. ["theme 1", "theme 2", "theme 3"])
"""


class ThemeSuggestionsPrompt:
    def __init__(self, start_location: str) -> None:
        self.start_location = start_location
        self.prompt_template = PromptTemplate(
            template=_PROMPT_TEMPLATE_TEXT,
            input_variables=['start_location'],
        )

    def get_prompt_text(self) -> str:
        return self.prompt_template.format_prompt(
            start_location=self.start_location
        ).to_string()

    def parse_model_output(self, model_output: str) -> List[str]:
        return json.loads(model_output)
