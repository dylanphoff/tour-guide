import logging
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from tour import Tour


logger = logging.getLogger(__name__)


_TOUR_ITINERARY_PROMPT_TEMPLATE_TEXT = """
    Create an itinerary for a walking tour.
    The tour should be described with a title and short description.
    Start location: {start_location}
    Approximate total distance in miles: {distance_mi}

    {theme_instructions}

    Stops
    There should be approximately {approx_stops} stops along the tour.
    Populate the entire list of stops with valid stops.
    If the start location is an interesting place, it should be the first stop.
    The number of stops can be slightly higher or lower depending on how much 
    information there is to cover in the area given the distance.
    These stops should be listed in the order in which they should be visited 
    with the order determined by travel efficiency and/or the logical flow of 
    information presented from one stop to the next.
    The location of each stop should include a title and specific GPS coordinates.
    Each stop should contain a teaser that the user will read before traveling 
    to it foreboding the information that will be covered. (e.g. for the first 
    stop: "First, we will go to x to learn about y", for middle stops: "Next, 
    we will visit x to see y", for the last stop: "Finally, we're headed to x, 
    where y occurred").
    The background of each stop should be in paragraph format and provide 
    interesting information about the location. The length of the background 
    should depend on the amount of relevant information.
    The key facts of each stop should cover other interesting facts that are 
    not covered in the background. The number of key facts should depend on the 
    amount of relevant information.

    Stop Activities
    For some of the stops, add activities to be perfomed.
    A stop can have no activities, a single activity, or multiple activities 
    depending on how well activities would fit the stop.
    An activity can be one of the following types and its content must match 
    the corresponding json schema exactly.

    Activity Types
    Type: trivia
    Description: A trivia question related to the stop with 4 options for the 
    answer and one being correct, indicated by correct_answer_index
    Content Schema: [
        question: str,
        answer_options: List[str],
        correct_answer_index: int,
    ]

    The response must be valid json. Do not output invalid nested quotes.

    {format_instructions}
"""

_THEME_INSTRUCTIONS_TEMPLATE_TEXT = """
    The theme of this tour is {theme}.
    The title and description of the tour should be relevant to the theme.
    The stops chosen and their accompanying information should be relevant to the theme.
    The tour stop activities chosen and their content should be relevant to the theme.
"""


class TourGenerationAssistant:
    def __init__(self):
        self.model = OpenAI(model_name="text-davinci-003", max_tokens=2056)
        self.tour_itinerary_output_parser = PydanticOutputParser(
            pydantic_object=Tour
        )
        self.tour_itinerary_prompt_template = PromptTemplate(
            template=_TOUR_ITINERARY_PROMPT_TEMPLATE_TEXT,
            input_variables=[
                "start_location",
                "distance_mi",
                "approx_stops",
                "theme",
            ],
            partial_variables={
                "format_instructions": (
                    self.tour_itinerary_output_parser.get_format_instructions()
                )
            },
        )

    def generate_tour(
        self,
        start_location: str,
        distance_mi: float,
        approx_stops: int,
        theme: str,
    ) -> Tour:
        if len(theme):
            theme_instructions = _THEME_INSTRUCTIONS_TEMPLATE_TEXT.format(
                theme=theme
            )
        else:
            theme_instructions = ""
        model_input = self.tour_itinerary_prompt_template.format_prompt(
            start_location=start_location,
            distance_mi=distance_mi,
            approx_stops=approx_stops,
            theme_instructions=theme_instructions,
        ).to_string()
        logging.debug("Model input: %s", model_input)
        model_output = self.model(model_input)
        logging.debug("Model output: %s", model_output)
        return self.tour_itinerary_output_parser.parse(model_output)

    def get_theme_suggestions(self, start_location):
        # TODO
        return []
