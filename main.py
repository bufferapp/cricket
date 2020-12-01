from typing import Text
from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from googleapiclient import discovery
from hatesonar import Sonar
import os

# Perspective API key
API_KEY = os.getenv("PERSPECTIVE_API_KEY")

# Initialize Sonar model
sonar = Sonar()

# Initialize Perspective API client
service = discovery.build("commentanalyzer", "v1alpha1", developerKey=API_KEY)


class TextRequest(BaseModel):
    text: str


# Start API
app = FastAPI(
    title="Cricket", description="Your personal Jiminy Cricket when posting online."
)


def handle_sonar_response(response):

    base_response = {"hate_speech": False, "offensive_language": False}

    if response.get("top_class") == "neither":
        return base_response

    classes = response.get("classes")

    for c in classes:
        if c.get("class_name") == "neither":
            continue
        if c.get("class_name") == "hate_speech" and c.get("confidence") > 0.7:
            base_response["hate_speech"] = True
        if c.get("class_name") == "offensive_language" and c.get("confidence") > 0.8:
            base_response["offensive_language"] = True

    return base_response


@app.post("/check/")
async def check(r: TextRequest):
    request = {
        "comment": {"text": r.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }

    try:
        perspective_response = service.comments().analyze(body=request).execute()
        sonar_response = sonar.ping(text=r.text)
    except Exception as e:
        response_json = {"Error": e}

    scores = perspective_response["attributeScores"]
    TOXICITY = scores["TOXICITY"]["summaryScore"]["value"] > 0.8
    IDENTITY_ATTACK = scores["IDENTITY_ATTACK"]["summaryScore"]["value"] > 0.8
    INSULT = scores["INSULT"]["summaryScore"]["value"] > 0.8
    PROFANITY = scores["PROFANITY"]["summaryScore"]["value"] > 0.8
    THREAT = scores["THREAT"]["summaryScore"]["value"] > 0.8
    SEXUALLY_EXPLICIT = scores["SEXUALLY_EXPLICIT"]["summaryScore"]["value"] > 0.8

    response_json = {
        "toxicity": TOXICITY,
        "identity_attack": IDENTITY_ATTACK,
        "insult": INSULT,
        "profanity": PROFANITY,
        "thread": THREAT,
        "sexually_explicit": SEXUALLY_EXPLICIT,
    }

    response_json.update(handle_sonar_response(sonar_response))
    return JSONResponse(content=response_json)
