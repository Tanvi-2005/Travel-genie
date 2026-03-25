"""
Database configuration and models for Travel Genie AI.
Uses SQLAlchemy with SQLite for persistent storage.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./travel_genie.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TripPlan(Base):
    """Stores user trip plans and generated itineraries."""
    __tablename__ = "trip_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    destination = Column(String(200), nullable=False)
    budget = Column(Float, nullable=False)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    duration_days = Column(Integer, nullable=False)
    travel_style = Column(String(50), nullable=False)  # adventure, relaxation, cultural, family
    interests = Column(String(500), nullable=True)
    language = Column(String(50), nullable=True, default="English")
    people = Column(Integer, nullable=False, default=1)
    generated_itinerary = Column(Text, nullable=True)
    ml_recommendation = Column(Text, nullable=True)
    ml_model_used = Column(String(100), nullable=True)
    satisfaction_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MLModelResult(Base):
    """Stores machine learning model comparison results."""
    __tablename__ = "ml_model_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    accuracy = Column(Float, nullable=False)
    precision_score = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    training_time_ms = Column(Float, nullable=False)
    tested_at = Column(DateTime, default=datetime.utcnow)


class TravelDataset(Base):
    """Stores the synthetic travel preference dataset."""
    __tablename__ = "travel_dataset"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    age = Column(Integer)
    budget = Column(Float)
    duration = Column(Integer)
    group_size = Column(Integer)
    travel_style_encoded = Column(Integer)  # 0=adventure, 1=relaxation, 2=cultural, 3=family
    preferred_climate = Column(Integer)     # 0=tropical, 1=temperate, 2=cold, 3=desert
    destination_category = Column(String(50))  # Target label


# Create all tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
