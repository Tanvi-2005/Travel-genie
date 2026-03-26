"""
Travel Genie AI - Main Flask Application
Personalized Trip Planning Assistant with Gemini AI and ML Model Comparison.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

from database import SessionLocal, TripPlan, MLModelResult, TravelDataset, Base, engine
from gemini_service import generate_itinerary
from weather_service import get_weather

# Load environment variables
load_dotenv()

app = Flask(__name__)
# CORS for frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialization logic on first request or app start
with app.app_context():
    print("🚀 Travel Genie AI starting up (Minimal Mode)...")
    Base.metadata.create_all(bind=engine)
    print("⚠️ ML Model training skipped (dependencies removed).")

# Global ML model state
ml_state = {
    "initialized": False,
    "best_model_name": "N/A"
}

# ─── Health Check ────────────────────────────────────────────────
@app.route("/")
def root():
    return jsonify({
        "message": "🌍 Travel Genie AI is running!",
        "ml_initialized": ml_state["initialized"],
        "best_model": ml_state.get("best_model_name", "N/A"),
    })

# ─── Weather Information ─────────────────────────────────────────
@app.route("/weather/<city>")
def get_weather_api(city):
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    if not WEATHER_API_KEY:
        return jsonify({"error": "API key missing"})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return jsonify({
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "city": data["name"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Legacy route for compatibility with query parameters
@app.route("/weather", methods=["GET"])
def fetch_weather():
    destination = request.args.get("destination")
    if not destination:
        return jsonify({"error": "Destination is required"}), 400
    return get_weather_api(destination)

# ─── Trip Planning ───────────────────────────────────────────────
@app.route("/plan-trip", methods=["POST"])
def plan_trip():
    """
    Plan a trip: generates a Gemini-powered itinerary.
    Stores everything in the database.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Calculate duration
    try:
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        duration_days = (end_date - start_date).days + 1
        if duration_days <= 0:
            duration_days = 1
    except (ValueError, TypeError):
        duration_days = 7

    # ML Recommendation (Disabled)
    ml_recommendation = "ML recommendation currently disabled."

    # Fetch weather context
    weather_info_str = ""
    weather = get_weather(data.get("destination"))
    if weather:
        weather_info_str = f"{weather['temp']}°C, {weather['description']}, Humidity: {weather['humidity']}%, Wind: {weather['wind_speed']} m/s"

    # Generate itinerary using Gemini
    itinerary = generate_itinerary(
        destination=data.get("destination"),
        budget=data.get("budget"),
        duration_days=duration_days,
        travel_style=data.get("travel_style"),
        interests=data.get("interests", ""),
        ml_recommendation=ml_recommendation,
        language=data.get("language", "English"),
        people=data.get("people", 1),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        weather_info=weather_info_str,
    )

    # Save to database
    db = SessionLocal()
    try:
        db_trip = TripPlan(
            user_name=data.get("user_name"),
            destination=data.get("destination"),
            budget=float(data.get("budget", 0)),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            duration_days=duration_days,
            travel_style=data.get("travel_style"),
            interests=data.get("interests"),
            language=data.get("language", "English"),
            people=int(data.get("people", 1)),
            generated_itinerary=itinerary,
            ml_recommendation=ml_recommendation,
            ml_model_used=ml_state.get("best_model_name", "N/A"),
            created_at=datetime.utcnow(),
        )
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        
        # Prepare response (FastAPI models were serialized automatically, Flask needs manual work)
        response_data = {
            "id": db_trip.id,
            "user_name": db_trip.user_name,
            "destination": db_trip.destination,
            "budget": db_trip.budget,
            "start_date": db_trip.start_date,
            "end_date": db_trip.end_date,
            "duration_days": db_trip.duration_days,
            "travel_style": db_trip.travel_style,
            "interests": db_trip.interests,
            "language": db_trip.language,
            "people": db_trip.people,
            "generated_itinerary": db_trip.generated_itinerary,
            "ml_recommendation": db_trip.ml_recommendation,
            "ml_model_used": db_trip.ml_model_used,
            "satisfaction_score": db_trip.satisfaction_score,
            "created_at": db_trip.created_at.isoformat()
        }
        return jsonify(response_data)
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        db.close()

# ─── Get All Trips ──────────────────────────────────────────────
@app.route("/trips", methods=["GET"])
def get_all_trips():
    """Retrieve all trip plans from the database."""
    db = SessionLocal()
    try:
        trips = db.query(TripPlan).order_by(TripPlan.created_at.desc()).all()
        return jsonify([{
            "id": t.id, "user_name": t.user_name, "destination": t.destination,
            "budget": t.budget, "start_date": t.start_date, "end_date": t.end_date,
            "duration_days": t.duration_days, "travel_style": t.travel_style,
            "interests": t.interests, "language": t.language, "people": t.people,
            "generated_itinerary": t.generated_itinerary, "ml_recommendation": t.ml_recommendation,
            "ml_model_used": t.ml_model_used, "satisfaction_score": t.satisfaction_score,
            "created_at": t.created_at.isoformat()
        } for t in trips])
    finally:
        db.close()

# ─── Get Single Trip ────────────────────────────────────────────
@app.route("/trips/<int:trip_id>", methods=["GET"])
def get_trip(trip_id):
    """Retrieve a specific trip plan."""
    db = SessionLocal()
    try:
        trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        return jsonify({
            "id": trip.id, "user_name": trip.user_name, "destination": trip.destination,
            "budget": trip.budget, "start_date": trip.start_date, "end_date": trip.end_date,
            "duration_days": trip.duration_days, "travel_style": trip.travel_style,
            "interests": trip.interests, "language": trip.language, "people": trip.people,
            "generated_itinerary": trip.generated_itinerary, "ml_recommendation": trip.ml_recommendation,
            "ml_model_used": trip.ml_model_used, "satisfaction_score": trip.satisfaction_score,
            "created_at": trip.created_at.isoformat()
        })
    finally:
        db.close()

# ─── Delete Trip ─────────────────────────────────────────────────
@app.route("/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    """Delete a trip plan."""
    db = SessionLocal()
    try:
        trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        db.delete(trip)
        db.commit()
        return jsonify({"message": "Trip deleted successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        db.close()

# ─── Submit Feedback ──────────────────────────────────────────────
@app.route("/trips/<int:trip_id>/feedback", methods=["POST"])
def submit_feedback(trip_id):
    """Update the satisfaction score (rating) for a trip."""
    score = request.args.get("satisfaction_score", type=float)
    if score is None:
         return jsonify({"error": "satisfaction_score query param required"}), 400
         
    db = SessionLocal()
    try:
        trip = db.query(TripPlan).filter(TripPlan.id == trip_id).first()
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        trip.satisfaction_score = score
        db.commit()
        return jsonify({"message": "Feedback submitted successfully", "trip_id": trip_id, "score": score})
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        db.close()

# ─── ML Model Comparison (Disabled) ──────────────────────────────
@app.route("/ml/comparison", methods=["GET"])
def get_ml_comparison():
    return jsonify({"best_model": "N/A", "models": []})

# ─── User Feedback Performance (Disabled) ────────────────────────
@app.route("/ml/user-performance", methods=["GET"])
def get_user_performance():
    return jsonify([])

# ─── Retrain Models (Disabled) ──────────────────────────────────
@app.route("/ml/retrain", methods=["POST"])
def retrain_models():
    return jsonify({"message": "ML training is currently disabled."})

# ─── Dataset Stats (Disabled) ───────────────────────────────────
@app.route("/dataset/stats", methods=["GET"])
def get_dataset_stats():
    return jsonify({
        "total_records": 0,
        "categories": {},
        "features": ["age", "budget", "duration", "group_size", "travel_style", "preferred_climate"],
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
