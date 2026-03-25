"""
Travel Genie AI - Main FastAPI Application
Personalized Trip Planning Assistant with Gemini AI and ML Model Comparison.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db, TripPlan, MLModelResult, TravelDataset, Base, engine
from schemas import TripRequest, TripResponse, MLModelResultResponse, MLComparisonResponse
from gemini_service import generate_itinerary
from ml_model_comparison import generate_synthetic_dataset, train_and_compare_models, predict_destination
from weather_service import get_weather

app = FastAPI(
    title="Travel Genie AI",
    description="AI-Powered Personalized Trip Planning Assistant",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ML model state
ml_state = {
    "scaler": None,
    "label_encoder": None,
    "best_model": None,
    "best_model_name": None,
    "results": None,
    "initialized": False,
}


@app.on_event("startup")
async def startup_event():
    """Initialize ML models and seed dataset on startup."""
    print("🚀 Travel Genie AI starting up...")
    Base.metadata.create_all(bind=engine)

    # Generate dataset and train models
    print("📊 Generating synthetic travel dataset...")
    dataset = generate_synthetic_dataset(n_samples=2000)

    print("🤖 Training and comparing ML models...")
    results, scaler, label_encoder, best_model = train_and_compare_models(dataset)

    ml_state["scaler"] = scaler
    ml_state["label_encoder"] = label_encoder
    ml_state["best_model"] = best_model
    ml_state["best_model_name"] = results[0]["model_name"]
    ml_state["results"] = results
    ml_state["initialized"] = True

    # Store results in database
    db = next(get_db())
    try:
        # Clear old results
        db.query(MLModelResult).delete()
        for r in results:
            db_result = MLModelResult(
                model_name=r["model_name"],
                accuracy=r["accuracy"],
                precision_score=r["precision_score"],
                recall=r["recall"],
                f1_score=r["f1_score"],
                training_time_ms=r["training_time_ms"],
            )
            db.add(db_result)

        # Store dataset in database
        db.query(TravelDataset).delete()
        for _, row in dataset.iterrows():
            db_row = TravelDataset(
                age=int(row['age']),
                budget=float(row['budget']),
                duration=int(row['duration']),
                group_size=int(row['group_size']),
                travel_style_encoded=int(row['travel_style']),
                preferred_climate=int(row['preferred_climate']),
                destination_category=str(row['destination_category']),
            )
            db.add(db_row)

        db.commit()
        print(f"✅ ML models trained. Best: {results[0]['model_name']} (F1: {results[0]['f1_score']:.4f})")
        print(f"📦 {len(dataset)} records stored in database.")
    except Exception as e:
        db.rollback()
        print(f"❌ Database seed error: {e}")
    finally:
        db.close()


# ─── Health Check ────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "🌍 Travel Genie AI is running!",
        "ml_initialized": ml_state["initialized"],
        "best_model": ml_state.get("best_model_name", "N/A"),
    }


# ─── Weather Information ─────────────────────────────────────────
@app.get("/api/weather")
async def fetch_weather(destination: str):
    """Fetch weather securely from the backend."""
    weather = get_weather(destination)
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found or API key missing.")
    return weather


# ─── Trip Planning ───────────────────────────────────────────────
@app.post("/api/plan-trip", response_model=TripResponse)
async def plan_trip(trip: TripRequest, db: Session = Depends(get_db)):
    """
    Plan a trip: runs ML prediction then generates a Gemini-powered itinerary.
    Stores everything in the database.
    """
    # Calculate duration
    try:
        start_date = datetime.strptime(trip.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(trip.end_date, "%Y-%m-%d")
        duration_days = (end_date - start_date).days + 1
        if duration_days <= 0:
            duration_days = 1
    except ValueError:
        duration_days = 7

    # ML Prediction
    ml_recommendation = ""
    if ml_state["initialized"]:
        user_features = {
            "age": 30,  # Default age since not collected in form
            "budget": trip.budget,
            "duration": duration_days,
            "group_size": trip.people,  # Updated from Default
            "travel_style": trip.travel_style,
            "preferred_climate": "tropical",  # Default
        }
        ml_recommendation = predict_destination(
            user_features,
            ml_state["scaler"],
            ml_state["label_encoder"],
            ml_state["best_model"]
        )

    # Fetch weather context
    weather_info_str = ""
    weather = get_weather(trip.destination)
    if weather:
        weather_info_str = f"{weather['temp']}°C, {weather['description']}, Humidity: {weather['humidity']}%, Wind: {weather['wind_speed']} m/s"

    # Generate itinerary using Gemini
    itinerary = generate_itinerary(
        destination=trip.destination,
        budget=trip.budget,
        duration_days=duration_days,
        travel_style=trip.travel_style,
        interests=trip.interests or "",
        ml_recommendation=ml_recommendation,
        language=trip.language or "English",
        people=trip.people,
        start_date=trip.start_date,
        end_date=trip.end_date,
        weather_info=weather_info_str,
    )

    # Save to database
    db_trip = TripPlan(
        user_name=trip.user_name,
        destination=trip.destination,
        budget=trip.budget,
        start_date=trip.start_date,
        end_date=trip.end_date,
        duration_days=duration_days,
        travel_style=trip.travel_style,
        interests=trip.interests,
        language=trip.language or "English",
        people=trip.people,
        generated_itinerary=itinerary,
        ml_recommendation=ml_recommendation,
        ml_model_used=ml_state.get("best_model_name", "N/A"),
        created_at=datetime.utcnow(),
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


# ─── Get All Trips ──────────────────────────────────────────────
@app.get("/api/trips", response_model=list[TripResponse])
async def get_all_trips(db: Session = Depends(get_db)):
    """Retrieve all trip plans from the database."""
    trips = db.query(TripPlan).order_by(TripPlan.created_at.desc()).all()
    return trips


# ─── Get Single Trip ────────────────────────────────────────────
@app.get("/api/trips/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific trip plan."""
    trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


# ─── Delete Trip ─────────────────────────────────────────────────
@app.delete("/api/trips/{trip_id}")
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete a trip plan."""
    trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}


# ─── Submit Feedback ──────────────────────────────────────────────
@app.post("/api/trips/{trip_id}/feedback")
async def submit_feedback(trip_id: int, satisfaction_score: float, db: Session = Depends(get_db)):
    """Update the satisfaction score (rating) for a trip."""
    trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip.satisfaction_score = satisfaction_score
    db.commit()
    return {"message": "Feedback submitted successfully", "trip_id": trip_id, "score": satisfaction_score}


# ─── ML Model Comparison ────────────────────────────────────────
@app.get("/api/ml/comparison", response_model=MLComparisonResponse)
async def get_ml_comparison(db: Session = Depends(get_db)):
    """Get the ML model comparison results."""
    results = db.query(MLModelResult).order_by(MLModelResult.f1_score.desc()).all()
    if not results:
        raise HTTPException(status_code=404, detail="No ML results available. Server may still be starting.")

    return MLComparisonResponse(
        best_model=results[0].model_name,
        models=[
            MLModelResultResponse(
                model_name=r.model_name,
                accuracy=r.accuracy,
                precision_score=r.precision_score,
                recall=r.recall,
                f1_score=r.f1_score,
                training_time_ms=r.training_time_ms,
            )
            for r in results
        ],
    )


# ─── User Feedback Performance ──────────────────────────────────
@app.get("/api/ml/user-performance")
async def get_user_performance(db: Session = Depends(get_db)):
    """Measure model performance based on historical user satisfaction scores."""
    from sqlalchemy import func
    
    # Aggregate data by model
    stats = db.query(
        TripPlan.ml_model_used,
        func.avg(TripPlan.satisfaction_score).label("avg_score"),
        func.count(TripPlan.id).label("total")
    ).filter(TripPlan.satisfaction_score.isnot(None)).group_by(TripPlan.ml_model_used).all()
    
    # Calculate success rate (score >= 4 is considered a success)
    # Using a simple subquery-friendly approach
    results = []
    for s in stats:
        # For each model, find how many times score was >= 4
        successes = db.query(TripPlan).filter(
            TripPlan.ml_model_used == s.ml_model_used,
            TripPlan.satisfaction_score >= 4
        ).count()
        
        accuracy = (successes / s.total) if s.total > 0 else 0
        results.append({
            "model_name": s.ml_model_used,
            "avg_satisfaction": round(float(s.avg_score), 2) if s.avg_score else 0,
            "total_reviews": s.total,
            "user_accuracy": round(accuracy * 100, 2)
        })
    
    # Sort by accuracy descending
    results.sort(key=lambda x: x['user_accuracy'], reverse=True)
    return results



# ─── Retrain Models ─────────────────────────────────────────────
@app.post("/api/ml/retrain")
async def retrain_models(db: Session = Depends(get_db)):
    """Retrain all ML models with fresh data."""
    dataset = generate_synthetic_dataset(n_samples=2000)
    results, scaler, label_encoder, best_model = train_and_compare_models(dataset)

    ml_state["scaler"] = scaler
    ml_state["label_encoder"] = label_encoder
    ml_state["best_model"] = best_model
    ml_state["best_model_name"] = results[0]["model_name"]
    ml_state["results"] = results
    ml_state["initialized"] = True

    # Update database
    db.query(MLModelResult).delete()
    for r in results:
        db_result = MLModelResult(
            model_name=r["model_name"],
            accuracy=r["accuracy"],
            precision_score=r["precision_score"],
            recall=r["recall"],
            f1_score=r["f1_score"],
            training_time_ms=r["training_time_ms"],
        )
        db.add(db_result)
    db.commit()

    return {"message": "Models retrained successfully", "best_model": results[0]["model_name"]}


# ─── Dataset Stats ──────────────────────────────────────────────
@app.get("/api/dataset/stats")
async def get_dataset_stats(db: Session = Depends(get_db)):
    """Get statistics about the stored travel dataset."""
    total = db.query(TravelDataset).count()
    categories = {}
    for row in db.query(TravelDataset.destination_category).distinct().all():
        cat = row[0]
        count = db.query(TravelDataset).filter(TravelDataset.destination_category == cat).count()
        categories[cat] = count

    return {
        "total_records": total,
        "categories": categories,
        "features": ["age", "budget", "duration", "group_size", "travel_style", "preferred_climate"],
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
