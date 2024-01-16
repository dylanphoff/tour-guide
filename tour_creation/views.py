import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from tour_creation.__init__ import tour_generation_agent
from tour_creation.tour_generator import TourGenerator
from tour_creation.tour_stop_activity_factory import TourStopActivityFactory


def extract_data(view_func):
    def wrapper(request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            return view_func(request, data)
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON format in request body"}
            return HttpResponse(
                json.dumps(error_response),
                content_type="application/json",
                status=400,
            )

    return wrapper


@require_GET
@extract_data
def theme_suggestions_view(request: HttpRequest, data: dict) -> HttpResponse:
    start_location = data.get("start_location")
    if not start_location:
        error_response = {"error": "Start location field is required"}
        return HttpResponse(
            json.dumps(error_response),
            content_type="application/json",
            status=400,
        )
    theme_suggestions = tour_generation_agent.get_theme_suggestions(
        start_location
    )
    response = {"theme_suggestions": theme_suggestions}
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_GET
@extract_data
def create_tour_view(request: HttpRequest, data: dict) -> HttpResponse:
    start_location = data.get("start_location")
    distance_mi = data.get("distance_mi")
    theme = data.get("theme")
    if not (start_location and distance_mi and theme):
        error_response = {
            "error": "Start location, distance, and theme fields are required"
        }
        return HttpResponse(
            json.dumps(error_response),
            content_type="application/json",
            status=400,
        )
    tour_stop_activity_factory = TourStopActivityFactory()
    tour_generator = TourGenerator(
        agent=tour_generation_agent,
        tour_stop_activity_factory=tour_stop_activity_factory,
    )
    tour = tour_generator.create_tour(
        start_location=start_location,
        distance_mi=distance_mi,
        theme=theme,
    )
    response = {"tour": tour.dict()}
    return HttpResponse(json.dumps(response), content_type="application/json")
