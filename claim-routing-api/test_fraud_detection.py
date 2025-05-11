import sys
import os
sys.path.append(os.path.abspath("."))

from app.modules.scoring_engine import ScoringEngine
from app.models.claim import ClaimData

# Test cases for fraud detection
test_cases = [
    {
        "name": "High-Risk Fraud Case",
        "claim_amount": 30000,
        "vehicle_brand": None,
        "region": "Naples",
        "warranty": "third-party liability",
        "age": None,
        "expected_fraud": True
    },
    {
        "name": "Medium-Risk Case",
        "claim_amount": 18000,
        "vehicle_brand": "BMW",
        "region": "Naples",
        "warranty": "third-party liability",
        "age": 65,
        "expected_fraud": False
    },
    {
        "name": "Low-Risk Case",
        "claim_amount": 5000,
        "vehicle_brand": "Toyota",
        "region": "Milan",
        "warranty": "comprehensive",
        "age": 45,
        "expected_fraud": False
    },
    {
        "name": "Missing Info Case",
        "claim_amount": 12000,
        "vehicle_brand": None,
        "region": None,
        "warranty": "third-party liability",
        "age": None,
        "expected_fraud": True
    }
]

print("Testing fraud detection functionality...\n")

for i, test in enumerate(test_cases):
    print(f"Test {i+1}: {test['name']}")
    
    # Create claim data
    claim_data = ClaimData(
        claim_amount_paid=test["claim_amount"],
        vehicle_brand=test["vehicle_brand"],
        claim_region=test["region"],
        warranty=test["warranty"],
        policyholder_age=test["age"]
    )
    
    # Detect fraud
    fraud_indicator = ScoringEngine.detect_fraud(claim_data)
    
    # Print results
    print(f"  Claim Amount: €{test['claim_amount']}")
    print(f"  Vehicle Brand: {test['vehicle_brand']}")
    print(f"  Region: {test['region']}")
    print(f"  Warranty: {test['warranty']}")
    print(f"  Age: {test['age']}")
    print(f"  Expected Fraud: {test['expected_fraud']}")
    print(f"  Actual Fraud: {fraud_indicator.is_potential_fraud}")
    print(f"  Fraud Score: {fraud_indicator.fraud_score:.2f}")
    print(f"  Fraud Indicators: {fraud_indicator.fraud_indicators}")
    
    # Check if result matches expected
    if fraud_indicator.is_potential_fraud == test["expected_fraud"]:
        print("  ✅ PASS")
    else:
        print("  ❌ FAIL")
    
    print("\n" + "-"*50 + "\n")

print("Fraud detection testing complete!")
