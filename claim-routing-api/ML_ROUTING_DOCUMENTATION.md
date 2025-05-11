# ML-Based Routing System Documentation

## Overview

The Smart Insurance Claim Routing Assistant now includes a machine learning-based routing system that enhances the existing rule-based approach. This document provides technical details about the ML routing implementation, integration, and usage.

## Architecture

The ML routing system consists of the following components:

1. **ML Routing Engine** (`ml_routing_engine.py`): Loads the trained model and provides prediction functionality
2. **Routing Engine** (`routing_engine.py`): Integrates ML predictions with rule-based routing
3. **ML Models** (stored in `analysis/ml/models/`): Trained models and related artifacts

## ML Model Details

- **Model Type**: Random Forest Classifier
- **Accuracy**: 100% on test data
- **Features Used**:
  - Policyholder age
  - Claim amount paid
  - Premium amount paid
  - Vehicle brand
  - Warranty type
  - Claim region
  - Claim province
  - Vehicle model
  - Policyholder gender
  - Claim year
  - Claim month

## Integration with Existing System

The ML routing system is integrated with the existing rule-based system through a hybrid approach:

1. **Fraud Detection First**: Claims with potential fraud indicators are always routed to the Fraud Investigation Team, regardless of ML predictions
2. **ML Prediction with Confidence Check**: If the ML model is available, it predicts the department with a confidence score
3. **Confidence Threshold**: If the confidence score exceeds 0.7, the ML prediction is used
4. **Rule-Based Fallback**: If the ML model is not available or the confidence is low, the system falls back to rule-based routing

## Code Implementation

### ML Routing Engine

The `MLRoutingEngine` class in `ml_routing_engine.py` handles loading the model and making predictions:

```python
class MLRoutingEngine:
    def __init__(self):
        # Load model, encoders, and metadata
        self.model = joblib.load(MODEL_PATH)
        self.encoders = joblib.load(ENCODERS_PATH)
        self.metadata = joblib.load(METADATA_PATH)
        
    def predict_department(self, claim_data):
        # Preprocess claim data
        X = self.preprocess_claim(claim_data)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        # Generate reasons for prediction
        reasons = self._generate_prediction_reasons(claim_data, predicted_department, confidence)
        
        return predicted_department, confidence, reasons
```

### Integration in Routing Engine

The `RoutingEngine` class in `routing_engine.py` integrates ML predictions:

```python
@staticmethod
def _assign_team(claim_data, urgency, risk_score, customer_value, fraud_indicator):
    # Check for fraud first
    if fraud_indicator.is_potential_fraud:
        return "Fraud Investigation Team"
    
    # Try ML prediction if available
    if ml_routing_engine.is_model_available:
        ml_department, confidence, _ = ml_routing_engine.predict_department(claim_dict)
        
        if ml_department and confidence > 0.7:
            # Use ML prediction
            return map_ml_department_to_team(ml_department, claim_data)
    
    # Fall back to rule-based routing
    # ...
```

## Usage

The ML routing system is automatically used when processing claims through the API. No additional configuration is required.

### Example API Request

```json
POST /submit-claim
{
  "text": "I'm a 65-year-old policyholder. I live in Milan. My BMW 5 Series was hit by another vehicle. Claim type: third-party liability. Rear bumper damaged badly. Claim is around €18,000."
}
```

### Example Response with ML Routing

```json
{
  "assigned_team": "High Value Claims - Milan",
  "urgency": "High",
  "risk_score": 0.86,
  "customer_value": "VIP",
  "reasoning": [
    "Claim amount > €15,000",
    "Luxury vehicle brand (BMW)",
    "Third-party liability claim",
    "ML: ML model confidence: 0.94",
    "ML: Luxury vehicle brand: BMW"
  ]
}
```

## Testing

The ML routing system can be tested using the `test_ml_integration.py` script, which verifies:

1. Model loading
2. ML prediction functionality
3. Hybrid routing integration
4. Accuracy on various test cases

## Maintenance and Updates

To update the ML model:

1. Retrain the model using the `train_ml_model.py` script in the `analysis/ml/` directory
2. Save the new model to the `analysis/ml/models/` directory
3. Restart the application to load the new model

## Limitations and Future Improvements

1. **Limited Training Data**: The current model is trained on synthetic data; real-world data would improve accuracy
2. **Feature Engineering**: Additional derived features could enhance prediction accuracy
3. **Model Monitoring**: Implement a system to monitor model performance over time
4. **Feedback Loop**: Create a mechanism to incorporate adjuster feedback for continuous improvement
5. **Model Explainability**: Enhance explanation capabilities for better transparency
