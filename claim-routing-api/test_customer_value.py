import sys
import os
sys.path.append(os.path.abspath("."))

from app.modules.scoring_engine import ScoringEngine
from app.models.claim import ClaimData

# Test cases for customer value calculation
test_cases = [
    {
        "name": "VIP Customer (Premium)",
        "premium": 900,
        "brand": "Toyota",
        "expected": "VIP"
    },
    {
        "name": "Premium Customer (Premium)",
        "premium": 600,
        "brand": "Honda",
        "expected": "Premium"
    },
    {
        "name": "Standard Customer (Premium)",
        "premium": 400,
        "brand": "Fiat",
        "expected": "Standard"
    },
    {
        "name": "VIP Customer (Brand)",
        "premium": None,
        "brand": "Ferrari",
        "expected": "VIP"
    },
    {
        "name": "Premium Customer (Brand)",
        "premium": None,
        "brand": "BMW",
        "expected": "Premium"
    },
    {
        "name": "Standard Customer (Brand)",
        "premium": None,
        "brand": "Ford",
        "expected": "Standard"
    }
]

print("Testing adjusted customer value thresholds...\n")

for i, test in enumerate(test_cases):
    print(f"Test {i+1}: {test['name']}")
    
    # Create claim data
    claim_data = ClaimData(
        premium_amount_paid=test["premium"],
        vehicle_brand=test["brand"]
    )
    
    # Calculate customer value
    customer_value, reasons = ScoringEngine.calculate_customer_value(claim_data)
    
    # Print results
    print(f"  Premium: {test['premium']}")
    print(f"  Brand: {test['brand']}")
    print(f"  Expected: {test['expected']}")
    print(f"  Actual: {customer_value}")
    print(f"  Reasons: {reasons}")
    
    # Check if result matches expected
    if customer_value == test["expected"]:
        print("  ✅ PASS")
    else:
        print("  ❌ FAIL")
    
    print("\n" + "-"*50 + "\n")

print("Customer value threshold testing complete!")
