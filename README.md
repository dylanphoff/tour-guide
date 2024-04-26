# Tour Guide

Tour Guide takes you on a personalized walking tour! It uses LLMs to generate a tour matching your specifications. Provide a starting location, distance you'd like to travel, and a theme, and Tour Guide produces a series of tour stops with interesting facts and activities including trivia questions and related AI generated images.

## Getting Started

1. Installation
```
# Clone the repo
git clone https://github.com/dylanphoff/tour-guide.git

# Move into the root directory
cd tour-guide

# Create a virtual environment and activate it
python3 -m venv venv && source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

2. Create a ```.env``` file in the root directory with the following contents
```
OPENAI_API_KEY = <your OpenAI key>
```

3. Start the application
```
python3 manage.py runserver
```

4. Open a new terminal window and make requests
```
# Get theme suggestions
curl -X GET -H "Content-Type: application/json" -d '{"start_location": "Example location"}' http://127.0.0.1:8000/create/theme_suggestions/

# Create tour
curl -X GET -H "Content-Type: application/json" -d '{"start_location": "Example location", "distance_mi": 2, "theme": "Example theme"}' http://127.0.0.1:8000/create/

```
There is currently no frontend, so this is the best way to interact with the application.

## Running tests

Execute the following command from the root directory to run the full test suite
```
pytest tests
```
