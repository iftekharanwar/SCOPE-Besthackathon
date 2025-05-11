"""
ML-based Routing Engine for Insurance Claims

This module provides machine learning-based routing capabilities for insurance claims.
It loads a pre-trained model and makes routing decisions based on claim features.
"""

import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

MODEL_DIR = Path("/home/ubuntu/insurance-claim-assistant/analysis/ml/models")
MODEL_PATH = MODEL_DIR / "best_model.joblib"
ENCODERS_PATH = MODEL_DIR / "label_encoders.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.joblib"

class MLRoutingEngine:
    """
    Machine Learning-based routing engine for insurance claims.
    
    This class loads a pre-trained model and uses it to predict the most appropriate
    department for handling an insurance claim based on its features.
    """
    
    def __init__(self):
        """Initialize the ML routing engine by loading the model and related artifacts."""
        self.model = None
        self.encoders = None
        self.metadata = None
        self.is_model_available = False
        
        try:
            if MODEL_PATH.exists() and ENCODERS_PATH.exists() and METADATA_PATH.exists():
                self.model = joblib.load(MODEL_PATH)
                self.encoders = joblib.load(ENCODERS_PATH)
                self.metadata = joblib.load(METADATA_PATH)
                self.is_model_available = True
                print(f"ML model loaded successfully from {MODEL_PATH}")
            else:
                print("ML model files not found. Falling back to rule-based routing.")
        except Exception as e:
            print(f"Error loading ML model: {e}")
    
    def preprocess_claim(self, claim_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess a claim for ML prediction.
        
        Args:
            claim_data: Dictionary containing claim information
            
        Returns:
            DataFrame with preprocessed features ready for model prediction
        """
        if not self.is_model_available:
            return None
        
        df = pd.DataFrame([claim_data])
        
        if 'claim_date' in df.columns:
            df = df.drop(columns=['claim_date'])
            
        if 'claim_date' in claim_data and claim_data['claim_date']:
            try:
                claim_date = pd.to_datetime(claim_data['claim_date'])
                df['claim_year'] = claim_date.year
                df['claim_month'] = claim_date.month
            except:
                df['claim_year'] = 2025
                df['claim_month'] = 1
        else:
            df['claim_year'] = 2025
            df['claim_month'] = 1
        
        required_features = self.metadata['features']
        for feature in required_features:
            feature_lower = feature.lower()
            if feature_lower not in df.columns:
                if feature.lower() == 'policyholder_age':
                    df[feature_lower] = claim_data.get('policyholder_age', 40)
                elif feature.lower() == 'policyholder_gender':
                    df[feature_lower] = claim_data.get('policyholder_gender', 'Unknown')
                elif feature.lower() == 'warranty':
                    df[feature_lower] = claim_data.get('warranty', 'Unknown')
                elif feature.lower() == 'claim_region':
                    df[feature_lower] = claim_data.get('claim_region', 'Unknown')
                elif feature.lower() == 'claim_province':
                    df[feature_lower] = claim_data.get('claim_province', 'Unknown')
                elif feature.lower() == 'vehicle_brand':
                    df[feature_lower] = claim_data.get('vehicle_brand', 'Unknown')
                elif feature.lower() == 'vehicle_model':
                    df[feature_lower] = claim_data.get('vehicle_model', 'Unknown')
                elif feature.lower() == 'claim_amount_paid':
                    df['claim_amount_paid'] = claim_data.get('claim_amount', 0)
                elif feature.lower() == 'premium_amount_paid':
                    df['premium_amount_paid'] = claim_data.get('premium_amount', 0)
                else:
                    df[feature_lower] = 0
        
        for col, encoder in self.encoders.items():
            col_lower = col.lower()
            if col_lower in df.columns:
                try:
                    df[col_lower] = encoder.transform(df[col_lower].astype(str))
                except:
                    df[col_lower] = 0
        
        df.columns = [col.upper() for col in df.columns]
        return df
    
    def predict_department(self, claim_data: Dict[str, Any]) -> Tuple[str, float, List[str]]:
        """
        Predict the most appropriate department for a claim using the ML model.
        
        Args:
            claim_data: Dictionary containing claim information
            
        Returns:
            Tuple containing:
            - Predicted department
            - Confidence score (probability)
            - List of reasons for the prediction
        """
        if not self.is_model_available:
            return None, 0.0, ["ML model not available"]
        
        X = self.preprocess_claim(claim_data)
        if X is None:
            return None, 0.0, ["Failed to preprocess claim data"]
        
        try:
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence = max(probabilities)
            
            if isinstance(prediction, str) and prediction in self.metadata.get('target_classes', []):
                predicted_department = prediction
            elif isinstance(prediction, (int, np.integer)):
                departments = self.metadata['target_classes']
                predicted_department = departments[prediction]
            else:
                predicted_department = str(prediction)
            
            reasons = self._generate_prediction_reasons(claim_data, predicted_department, confidence)
            
            return predicted_department, confidence, reasons
        except Exception as e:
            print(f"Error making ML prediction: {e}")
            return None, 0.0, [f"Error in ML prediction: {str(e)}"]
    
    def _generate_prediction_reasons(self, claim_data: Dict[str, Any], 
                                    department: str, confidence: float) -> List[str]:
        """
        Generate human-readable reasons for the department prediction.
        
        Args:
            claim_data: Dictionary containing claim information
            department: Predicted department
            confidence: Prediction confidence
            
        Returns:
            List of reasons for the prediction
        """
        reasons = []
        
        reasons.append(f"ML model confidence: {confidence:.2f}")
        
        if department == "High Value Claims":
            if claim_data.get('claim_amount', 0) > 5000:
                reasons.append(f"Claim amount (€{claim_data.get('claim_amount', 0)}) exceeds €5,000")
            
            if claim_data.get('vehicle_brand', '').lower() in ['bmw', 'mercedes', 'audi', 'porsche']:
                reasons.append(f"Luxury vehicle brand: {claim_data.get('vehicle_brand', '')}")
        
        elif department == "Legal Claims":
            if 'third-party' in str(claim_data.get('warranty', '')).lower():
                reasons.append("Third-party liability warranty")
        
        elif department == "Senior Claims":
            if claim_data.get('policyholder_age', 0) > 65:
                reasons.append(f"Policyholder age ({claim_data.get('policyholder_age', 0)}) exceeds 65 years")
        
        elif department == "VIP Claims":
            if claim_data.get('premium_amount', 0) > 400:
                reasons.append(f"Premium amount (€{claim_data.get('premium_amount', 0)}) exceeds €400")
        
        elif department == "Regional Team - South":
            if claim_data.get('claim_region', '') in ['Napoli', 'Naples', 'Caserta']:
                reasons.append(f"Claim from southern region: {claim_data.get('claim_region', '')}")
        
        if len(reasons) == 1:  # Only confidence reason
            reasons.append("Based on overall claim characteristics")
        
        return reasons

ml_routing_engine = MLRoutingEngine()
