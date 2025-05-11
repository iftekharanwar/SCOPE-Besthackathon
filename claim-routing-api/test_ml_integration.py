"""
Test script for ML model integration with the routing engine.

This script tests the ML-based routing functionality by submitting sample claims
and verifying that the ML model correctly routes them to appropriate departments.
"""

import sys
import os
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.models.claim import ClaimData
from app.modules.routing_engine import RoutingEngine
from app.modules.ml_routing_engine import ml_routing_engine

def test_ml_model_loading():
    """Test that the ML model is loaded correctly."""
    print("\n=== Testing ML Model Loading ===")
    print(f"ML model available: {ml_routing_engine.is_model_available}")
    
    if ml_routing_engine.is_model_available:
        print("✅ ML model loaded successfully")
        print(f"Model type: {type(ml_routing_engine.model).__name__}")
        print(f"Number of features: {len(ml_routing_engine.metadata['features'])}")
        print(f"Target classes: {ml_routing_engine.metadata['target_classes']}")
    else:
        print("❌ ML model not loaded")
    
    return ml_routing_engine.is_model_available

def test_ml_prediction(claim_data_dict):
    """Test ML prediction functionality."""
    print("\n=== Testing ML Prediction ===")
    
    department, confidence, reasons = ml_routing_engine.predict_department(claim_data_dict)
    
    print(f"Predicted department: {department}")
    print(f"Confidence: {confidence:.4f}")
    print("Reasons:")
    for reason in reasons:
        print(f"  - {reason}")
    
    if department and confidence > 0:
        print("✅ ML prediction successful")
    else:
        print("❌ ML prediction failed")
    
    return department, confidence, reasons

def test_hybrid_routing(claim_data_dict):
    """Test hybrid routing with ML and rule-based approaches."""
    print("\n=== Testing Hybrid Routing ===")
    
    claim_data = ClaimData(**claim_data_dict)
    
    decision = RoutingEngine.route_claim(claim_data)
    
    print(f"Assigned team: {decision.assigned_team}")
    print(f"Urgency: {decision.urgency}")
    print(f"Risk score: {decision.risk_score:.4f}")
    print(f"Customer value: {decision.customer_value}")
    print("Reasoning:")
    for reason in decision.reasoning:
        print(f"  - {reason}")
    
    ml_reasons = [r for r in decision.reasoning if r.startswith("ML:")]
    if ml_reasons:
        print("✅ ML reasoning included in decision")
    else:
        print("⚠️ No ML reasoning in decision")
    
    return decision

def run_tests():
    """Run all ML integration tests."""
    print("=== ML Integration Tests ===")
    
    model_loaded = test_ml_model_loading()
    if not model_loaded:
        print("\n❌ ML model not available. Skipping remaining tests.")
        return
    
    test_cases = [
        {
            "name": "High-value luxury vehicle claim",
            "data": {
                "policyholder_age": 45,
                "policyholder_gender": "Male",
                "warranty": "Comprehensive",
                "claim_region": "Milan",
                "claim_province": "Lombardy",
                "vehicle_brand": "BMW",
                "vehicle_model": "5 Series",
                "claim_amount_paid": 18000,
                "premium_amount_paid": 1200,
                "claim_date": "2025-04-15"
            },
            "expected_department": "High Value Claims"
        },
        {
            "name": "Senior policyholder claim",
            "data": {
                "policyholder_age": 72,
                "policyholder_gender": "Female",
                "warranty": "Basic",
                "claim_region": "Rome",
                "claim_province": "Lazio",
                "vehicle_brand": "Fiat",
                "vehicle_model": "Panda",
                "claim_amount_paid": 3500,
                "premium_amount_paid": 450,
                "claim_date": "2025-04-10"
            },
            "expected_department": "Senior Claims"
        },
        {
            "name": "Legal third-party claim",
            "data": {
                "policyholder_age": 35,
                "policyholder_gender": "Male",
                "warranty": "Third-party liability",
                "claim_region": "Naples",
                "claim_province": "Campania",
                "vehicle_brand": "Alfa Romeo",
                "vehicle_model": "Giulia",
                "claim_amount_paid": 7500,
                "premium_amount_paid": 800,
                "claim_date": "2025-04-20"
            },
            "expected_department": "Legal Claims"
        },
        {
            "name": "VIP customer claim",
            "data": {
                "policyholder_age": 50,
                "policyholder_gender": "Female",
                "warranty": "Premium",
                "claim_region": "Turin",
                "claim_province": "Piedmont",
                "vehicle_brand": "Mercedes",
                "vehicle_model": "E-Class",
                "claim_amount_paid": 9000,
                "premium_amount_paid": 1500,
                "claim_date": "2025-04-25"
            },
            "expected_department": "VIP Claims"
        },
        {
            "name": "Standard claim",
            "data": {
                "policyholder_age": 28,
                "policyholder_gender": "Male",
                "warranty": "Basic",
                "claim_region": "Florence",
                "claim_province": "Tuscany",
                "vehicle_brand": "Renault",
                "vehicle_model": "Clio",
                "claim_amount_paid": 1200,
                "premium_amount_paid": 350,
                "claim_date": "2025-04-30"
            },
            "expected_department": "Standard Claims"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n\n=== Test Case {i+1}: {test_case['name']} ===")
        
        department, confidence, reasons = test_ml_prediction(test_case['data'])
        
        if department and department.startswith(test_case['expected_department']):
            print(f"✅ ML prediction matches expected department: {test_case['expected_department']}")
        else:
            print(f"❌ ML prediction does not match expected department: {test_case['expected_department']}")
        
        decision = test_hybrid_routing(test_case['data'])
        
        print("\n" + "-" * 50)

if __name__ == "__main__":
    run_tests()
