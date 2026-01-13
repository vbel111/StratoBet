"""
Database models - reuse from ML pipeline
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class HistoricalMatch(Base):
    """Historical match data"""
    __tablename__ = 'matches_historical'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    league = Column(String(50), nullable=False)
    league_code = Column(String(10))
    season = Column(String(10))
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
    total_goals = Column(Integer, nullable=False)
    result = Column(String(10))
    home_shots = Column(Integer)
    away_shots = Column(Integer)
    home_shots_on_target = Column(Integer)
    away_shots_on_target = Column(Integer)
    home_odds = Column(Float)
    draw_odds = Column(Float)
    away_odds = Column(Float)
    over_25_odds = Column(Float)
    under_25_odds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
