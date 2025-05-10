import re
from typing import Dict, Any, Optional
import json
from app.models.claim import ClaimData


class ClaimExtractor:
    """Extract claim data from text or structured input"""

    @staticmethod
    def extract_from_text(text: str) -> ClaimData:
        """Extract claim data from natural language text"""
        claim_data = ClaimData(raw_text=text)

        age_match = re.search(r'(\d+)[\s-]*year[\s-]*old', text, re.IGNORECASE)
        if age_match:
            claim_data.policyholder_age = int(age_match.group(1))

        regions = ["Milan", "Rome", "Naples", "Turin", "Palermo", "Genoa", "Bologna", 
                  "Florence", "Bari", "Catania", "Napoli", "Caserta"]
        for region in regions:
            if re.search(rf'\b{region}\b', text, re.IGNORECASE):
                claim_data.claim_region = region
                break

        warranty_types = ["third-party liability", "third party liability", "comprehensive", 
                         "collision", "fire and theft", "personal injury"]
        for warranty in warranty_types:
            if re.search(rf'\b{warranty}\b', text, re.IGNORECASE):
                claim_data.warranty = warranty
                break

        brands = ["BMW", "Mercedes", "Audi", "Volkswagen", "Toyota", "Honda", "Ford", 
                 "Fiat", "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo"]
        for brand in brands:
            if re.search(rf'\b{brand}\b', text, re.IGNORECASE):
                claim_data.vehicle_brand = brand
                break

        amount_match = re.search(r'(?:claim|amount|cost|worth|around|approximately).*?(?:€|EUR|euro|[$])\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)|(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)\s*(?:thousand|k|€|EUR|euro)', text, re.IGNORECASE)
        if amount_match:
            amount_str = amount_match.group(1) if amount_match.group(1) else amount_match.group(2)
            amount_str = amount_str.replace(',', '')
            amount = float(amount_str)
            
            if 'thousand' in text.lower() or 'k' in text.lower():
                if amount < 100:  # Likely specified in thousands
                    amount *= 1000
            
            claim_data.claim_amount_paid = amount

        return claim_data

    @staticmethod
    def extract_from_json(data: Dict[str, Any]) -> ClaimData:
        """Extract claim data from structured JSON input"""
        claim_data = ClaimData()
        
        field_mapping = {
            "POLICYHOLDER_AGE": "policyholder_age",
            "WARRANTY": "warranty",
            "CLAIM_AMOUNT_PAID": "claim_amount_paid",
            "PREMIUM_AMOUNT_PAID": "premium_amount_paid",
            "CLAIM_REGION": "claim_region",
            "CLAIM_PROVINCE": "claim_province",
            "VEHICLE_BRAND": "vehicle_brand",
            "VEHICLE_MODEL": "vehicle_model",
            "POLICYHOLDER_GENDER": "policyholder_gender",
            "CLAIM_ID": "claim_id",
            "CLAIM_DATE": "claim_date"
        }
        
        for json_field, model_field in field_mapping.items():
            if json_field in data:
                setattr(claim_data, model_field, data[json_field])
                
        return claim_data

    @staticmethod
    def extract(input_data: Dict[str, Any]) -> ClaimData:
        """Extract claim data from either text or structured input"""
        if "text" in input_data and input_data["text"]:
            return ClaimExtractor.extract_from_text(input_data["text"])
        elif "structured_data" in input_data and input_data["structured_data"]:
            return ClaimExtractor.extract_from_json(input_data["structured_data"])
        else:
            raise ValueError("Input must contain either 'text' or 'structured_data'")
