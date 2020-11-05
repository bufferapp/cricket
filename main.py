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
app = FastAPI()


@app.post("/sonar/")
async def sonar_endpoint(sonar_request: TextRequest):
    response = sonar.ping(text=sonar_request.text)
    return JSONResponse(content=response)


@app.post("/perspective/")
async def perspective_endpoint(sonar_request: TextRequest):
    request = {
        "comment": {"text": sonar_request.text},
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
        sonar_response = sonar.ping(text=sonar_request.text)
    except Exception as e:
        response_json = {"Error": e}

    scores = perspective_response["attributeScores"]
    TOXICITY = scores["TOXICITY"]["summaryScore"]["value"]
    IDENTITY_ATTACK = scores["IDENTITY_ATTACK"]["summaryScore"]["value"]
    INSULT = scores["INSULT"]["summaryScore"]["value"]
    PROFANITY = scores["PROFANITY"]["summaryScore"]["value"]
    THREAT = scores["THREAT"]["summaryScore"]["value"]
    SEXUALLY_EXPLICIT = scores["SEXUALLY_EXPLICIT"]["summaryScore"]["value"]
    response_json = {
        "toxicity": TOXICITY,
        "identity_attack": IDENTITY_ATTACK,
        "insult": INSULT,
        "profanity": PROFANITY,
        "thread": THREAT,
        "sexually_explicit": SEXUALLY_EXPLICIT,
    }
    return JSONResponse(content=response_json)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "alive"}
