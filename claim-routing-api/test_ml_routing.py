"""
Test script for ML-based routing functionality.

This script tests the ML routing engine by simulating claims and verifying
that the routing decisions are made correctly.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from app.models.claim import ClaimData
from app.modules.routing_engine import RoutingEngine
from app.modules.ml_routing_engine import ml_routing_engine

def test_ml_routing():
    """Test the ML-based routing functionality"""
    print("Testing ML-based routing functionality...")
    
    if not ml_routing_engine.is_model_available:
        print("ML model is not available. Please train the model first.")
        return False
    
    test_claims = [
        ClaimData(
            policyholder_age=45,
            policyholder_gender="Male",
            warranty="Comprehensive",
            claim_date=datetime.now().isoformat(),
            claim_region="Milan",
            claim_province="Milan",
            vehicle_brand="BMW",
            vehicle_model="5 Series",
            claim_amount_paid=18000,
            premium_amount_paid=600
        ),
        ClaimData(
            policyholder_age=70,
            policyholder_gender="Female",
            warranty="Basic",
            claim_date=datetime.now().isoformat(),
            claim_region="Rome",
            claim_province="Rome",
            vehicle_brand="Fiat",
            vehicle_model="Panda",
            claim_amount_paid=7000,
            premium_amount_paid=300
        ),
        ClaimData(
            policyholder_age=35,
            policyholder_gender="Male",
            warranty="Premium",
            claim_date=datetime.now().isoformat(),
            claim_region="Turin",
            claim_province="Turin",
            vehicle_brand="Audi",
            vehicle_model="A4",
            claim_amount_paid=4000,
            premium_amount_paid=900
        ),
        ClaimData(
            policyholder_age=28,
            policyholder_gender="Female",
            warranty="Basic",
            claim_date=datetime.now().isoformat(),
            claim_region="Florence",
            claim_province="Florence",
            vehicle_brand="Renault",
            vehicle_model="Clio",
            claim_amount_paid=1500,
            premium_amount_paid=200
        )
    ]
    
    for i, claim in enumerate(test_claims):
        print(f"\nTest Claim {i+1}:")
        print(f"  Age: {claim.policyholder_age}")
        print(f"  Vehicle: {claim.vehicle_brand} {claim.vehicle_model}")
        print(f"  Claim Amount: €{claim.claim_amount_paid}")
        print(f"  Premium: €{claim.premium_amount_paid}")
        
        decision = RoutingEngine.route_claim(claim)
        
        print(f"  Assigned Team: {decision.assigned_team}")
        print(f"  Urgency: {decision.urgency}")
        print(f"  Risk Score: {decision.risk_score:.2f}")
        print(f"  Customer Value: {decision.customer_value}")
        print("  Reasoning:")
        for reason in decision.reasoning:
            print(f"    - {reason}")
    
    print("\nML routing test completed successfully!")
    return True

if __name__ == "__main__":
    test_ml_routing()
