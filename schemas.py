"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TripRequest(BaseModel):
    user_name: str
    destination: str
    budget: float
    start_date: str
    end_date: str
    travel_style: str  # adventure, relaxation, cultural, family
    interests: Optional[str] = None
    language: Optional[str] = "English"
    people: int = 1


class TripResponse(BaseModel):
    id: int
    user_name: str
    destination: str
    budget: float
    start_date: str
    end_date: str
    duration_days: int
    travel_style: str
    interests: Optional[str]
    language: Optional[str] = "English"
    people: int = 1
    generated_itinerary: Optional[str]
    ml_recommendation: Optional[str]
    ml_model_used: Optional[str]
    satisfaction_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class MLModelResultResponse(BaseModel):
    model_name: str
    accuracy: float
    precision_score: float
    recall: float
    f1_score: float
    training_time_ms: float

    class Config:
        from_attributes = True


class MLComparisonResponse(BaseModel):
    best_model: str
    models: list[MLModelResultResponse]
