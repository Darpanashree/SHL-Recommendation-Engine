from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .model import recommend_assessments
import logging

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific frontend origins
    allow_methods=["GET", "POST"],  # Restrict to necessary methods
    allow_headers=["*"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Received query: {query}")
        results = recommend_assessments(query)
        if not results:
            logger.warning(f"No recommendations found for query: {query}")
            raise HTTPException(status_code=404, detail="No recommendations found.")
        logger.info(f"Returning recommendations: {results}")
        return {"recommendations": results}
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
