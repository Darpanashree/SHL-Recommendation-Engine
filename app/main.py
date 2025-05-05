from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .model import recommend_assessments

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class RecommendationResponse(BaseModel):
    recommendations: List[str]

@app.get("/recommend", response_model=RecommendationResponse)
async def recommend(query: str):
    results = recommend_assessments(query)
    return {"recommendations": results}
