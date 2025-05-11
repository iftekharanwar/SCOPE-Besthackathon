import sys
import os
sys.path.append(os.path.abspath("."))

from app.modules.claim_extractor import ClaimExtractor

# Test cases
test_cases = [
    {
        "name": "Basic claim",
        "text": "I'm a 65-year-old policyholder. I live in Milan. My BMW 5 Series was hit by another vehicle. Claim type: third-party liability. Rear bumper damaged badly. Claim is around €18,000."
    },
    {
        "name": "Different format",
        "text": "Policyholder age 42, residing in Naples. Mercedes C-Class damaged in collision. Premium paid €1200. Claim amount: 8500 euros."
    },
    {
        "name": "Minimal information",
        "text": "Ferrari crashed in Rome. 35 year old driver. Comprehensive insurance. Repair costs 25k."
    }
]

print("Testing NLP-enhanced claim extraction...\n")

for i, test in enumerate(test_cases):
    print(f"Test {i+1}: {test['name']}")
    print(f"Input: {test['text']}")
    
    # Extract claim data
    claim_data = ClaimExtractor.extract_from_text(test["text"])
    
    # Print extracted data
    print("\nExtracted data:")
    print(f"  Age: {claim_data.policyholder_age}")
    print(f"  Region: {claim_data.claim_region}")
    print(f"  Warranty: {claim_data.warranty}")
    print(f"  Vehicle Brand: {claim_data.vehicle_brand}")
    print(f"  Vehicle Model: {claim_data.vehicle_model}")
    print(f"  Claim Amount: {claim_data.claim_amount_paid}")
    print("\n" + "-"*50 + "\n")

print("NLP testing complete!")
