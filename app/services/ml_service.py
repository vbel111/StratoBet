"""
ML Model Service
Loads and manages the trained ML model for predictions
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
from app.core.config import settings


class MLModelService:
    """Service for loading and using the trained ML model"""
    
    def __init__(self):
        self.model = None
        self.model_data = None
        self.feature_names = None
        self.model_version = None
        self.last_prediction_at = None
        
    def load_model(self) -> bool:
        """Load the trained model from disk"""
        try:
            model_path = Path(settings.MODEL_PATH)
            
            if not model_path.exists():
                print(f"Model file not found: {model_path}")
                return False
            
            # Load model data (contains model + metadata)
            self.model_data = joblib.load(model_path)
            
            # Extract components
            self.model = self.model_data['model']
            self.feature_names = self.model_data['feature_names']
            self.model_version = self.model_data['version']
            
            print(f"✅ Model loaded successfully!")
            print(f"   Version: {self.model_version}")
            print(f"   Features: {len(self.feature_names)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def predict(self, features: Dict[str, float]) -> Tuple[float, float, float]:
        """
        Make a prediction given features.
        
        Args:
            features: Dictionary of feature names to values
        
        Returns:
            Tuple of (over_25_prob, under_25_prob, confidence_score)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Convert features dict to numpy array in correct order
        feature_vector = np.array([features.get(name, 0.0) for name in self.feature_names]).reshape(1, -1)
        
        # Get probabilities
        probabilities = self.model.predict_proba(feature_vector)[0]
        
        under_25_prob = float(probabilities[0])
        over_25_prob = float(probabilities[1])
        
        # Calculate confidence (how far from 50/50)
        confidence = abs(over_25_prob - 0.5) * 2
        
        # Update last prediction time
        self.last_prediction_at = datetime.utcnow()
        
        return over_25_prob, under_25_prob, confidence
    
    def get_confidence_level(self, confidence_score: float) -> str:
        """Convert confidence score to readable level"""
        if confidence_score < 0.3:
            return "Low"
        elif confidence_score < 0.6:
            return "Medium"
        elif confidence_score < 0.85:
            return "High"
        else:
            return "Very High"
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    def get_info(self) -> Dict:
        """Get model information"""
        return {
            "model_loaded": self.is_loaded(),
            "model_version": self.model_version or "unknown",
            "model_path": settings.MODEL_PATH,
            "features_count": len(self.feature_names) if self.feature_names else 0,
            "last_prediction_at": self.last_prediction_at
        }


# Global model service instance
ml_service = MLModelService()
