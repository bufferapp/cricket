import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from detoxify import Detoxify


class TextRequest(BaseModel):
    text: str


# Start API
app = FastAPI(
    title="Cricket", description="Your personal Jiminy Cricket when posting online."
)

model = Detoxify("original")


@app.post("/check/")
async def check(r: TextRequest):
    response = model.predict(r.text)

    response_json = {
        "toxicity": float(response["toxicity"]),
        "severe_toxicity": float(response["severe_toxicity"]),
        "obscene": float(response["obscene"]),
        "threat": float(response["threat"]),
        "insult": float(response["insult"]),
        "identity_hate": float(response["identity_hate"]),
    }
    return JSONResponse(content=response_json)
