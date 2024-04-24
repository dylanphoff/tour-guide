from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from common.tour import Tour


_PROMPT_TEMPLATE_TEXT = """
Create an itinerary for a walking tour.
The tour should be described with a title and short description.
Start location: {start_location}
Approximate total distance in miles: {distance_mi}

{theme_instructions}

Stops
- There should be approximately {approx_stops} stops along the tour.
- Populate the entire list of stops with valid stops.
- The location of each stop must be as specific as possible so there is no 
ambiguity about where to stand (e.g. if the location is a building, the 
location must specify exactly where around or in the building the users should 
stand to give the related information the best context).
- If the start location is an interesting place, it should be the first stop.
- The number of stops can be slightly higher or lower depending on how much 
information there is to cover in the area given the distance.
- These stops should be listed in the order in which they should be visited 
with the order determined by travel efficiency and/or the logical flow of 
information presented from one stop to the next.
- Each stop should contain a teaser that the user will read before traveling 
to it foreboding the information that will be covered. (e.g. for the first 
stop: "First, we will go to x to learn about y", for middle stops: "Next, 
we will visit x to see y", for the last stop: "Finally, we're headed to x, 
where y occurred").
- The background of each stop should be in paragraph format and provide 
interesting information about the location. The length of the background 
should depend on the amount of relevant information.
- The key facts of each stop should cover other interesting facts that are 
not covered in the background. The number of key facts should depend on the 
amount of relevant information.

Stop Activities
- For some of the stops, add activities to be perfomed.
- Add the activities to the 'activities' field, always filling 
'executable_activities' with an empty list.
- A stop can have no activities, a single activity, or multiple activities 
depending on how well activities would fit the stop.
- An activity can be one of the following types and its content must match 
the corresponding json schema exactly.

Activity Types
Type: trivia
Description: A trivia question related to the stop with 4 options for the 
answer and one being correct, indicated by correct_answer_index. Do not 
make the trivia question a question who's answer is revealed in the background 
or key facts.
Content Schema: [
    question: str,
    answer_options: List[str],
    correct_answer_index: int,
]
Type: image
Description: An image of a scene relevant to the stop, accounting for the 
theme and period the tour covers. The prompt field is a prompt for an AI model 
to generate this image and the description field is a description that 
accurately describes the generated image
Content Schema: [
    prompt: str,
    description: str,
]

The response must be valid JSON. Only use single quotes within the values.

{format_instructions}
"""

_THEME_INSTRUCTIONS_TEMPLATE_TEXT = """
Theme
- The theme of this tour is {theme}.
- The title and description of the tour should be relevant to the theme.
- The stops chosen and their accompanying information should be relevant to the theme.
- The tour stop activities chosen and their content should be relevant to the theme.
"""


class TourGenerationPrompt:
    def __init__(
        self,
        start_location: str,
        distance_mi: float,
        approx_stops: int,
        theme: str,
    ) -> None:
        self.start_location = start_location
        self.distance_mi = distance_mi
        self.approx_stops = approx_stops
        self.theme = theme
        self.output_parser = PydanticOutputParser(
            pydantic_object=Tour
        )
        self.prompt_template = PromptTemplate(
            template=_PROMPT_TEMPLATE_TEXT,
            input_variables=[
                'start_location',
                'distance_mi',
                'approx_stops',
                'theme',
            ],
            partial_variables={
                'format_instructions': (
                    self.output_parser.get_format_instructions()
                )
            },
        )

    def get_prompt_text(self) -> str:
        if len(self.theme):
            theme_instructions = _THEME_INSTRUCTIONS_TEMPLATE_TEXT.format(
                theme=self.theme
            )
        else:
            theme_instructions = ""
        return self.prompt_template.format_prompt(
            start_location=self.start_location,
            distance_mi=self.distance_mi,
            approx_stops=self.approx_stops,
            theme_instructions=theme_instructions,
        ).to_string()

    def parse_model_output(self, model_output: str) -> Tour:
        return self.output_parser.parse(model_output)
