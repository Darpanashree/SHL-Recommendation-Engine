from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .model import recommend_assessments

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific frontend origins
    allow_methods=["GET", "POST"],  # Restrict to necessary methods
    allow_headers=["*"]
)

class RecommendationResponse(BaseModel):
    recommendations: List[str]

@app.get(
    "/recommend", 
    response_model=RecommendationResponse,
    summary="Get Recommendations",
    description="Provide a query to get a list of recommended assessments."
)
async def recommend(query: str = Query(..., min_length=1, description="Search query for recommendations")):
    try:
        results = recommend_assessments(query)
        if not results:
            raise HTTPException(status_code=404, detail="No recommendations found.")
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
