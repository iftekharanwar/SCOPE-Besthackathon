import re
from typing import Dict, Any, Optional
import json
import spacy
from app.models.claim import ClaimData


class ClaimExtractor:
    """Extract claim data from text or structured input"""
    
    nlp = spacy.load("en_core_web_sm")
    
    regions = ["Milan", "Rome", "Naples", "Turin", "Palermo", "Genoa", "Bologna", 
              "Florence", "Bari", "Catania", "Napoli", "Caserta"]
    
    warranty_types = ["third-party liability", "third party liability", "comprehensive", 
                     "collision", "fire and theft", "personal injury"]
    
    brands = ["BMW", "Mercedes", "Audi", "Volkswagen", "Toyota", "Honda", "Ford", 
             "Fiat", "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo"]
    
    models = {
        "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i4", "i8", "iX"],
        "Mercedes": ["A-Class", "B-Class", "C-Class", "E-Class", "S-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "G-Class", "CLA", "CLS", "SL", "AMG GT"],
        "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "e-tron"],
        "Volkswagen": ["Golf", "Polo", "Passat", "Tiguan", "T-Roc", "T-Cross", "Touareg", "ID.3", "ID.4", "Arteon"],
        "Toyota": ["Yaris", "Corolla", "Camry", "RAV4", "C-HR", "Prius", "Land Cruiser", "Hilux", "Aygo", "Supra"],
        "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Jazz", "NSX", "e"],
        "Ford": ["Fiesta", "Focus", "Mondeo", "Kuga", "Puma", "Mustang", "Explorer", "Ranger", "Transit"],
        "Fiat": ["500", "Panda", "Tipo", "500X", "500L"],
        "Ferrari": ["F8", "Roma", "SF90", "812", "Portofino", "Purosangue"],
        "Lamborghini": ["Aventador", "Huracan", "Urus"],
        "Maserati": ["Ghibli", "Levante", "Quattroporte", "MC20"],
        "Alfa Romeo": ["Giulia", "Stelvio", "Tonale"]
    }

    @staticmethod
    def extract_from_text(text: str) -> ClaimData:
        """Extract claim data from natural language text using NLP"""
        claim_data = ClaimData(raw_text=text)
        
        doc = ClaimExtractor.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ == "CARDINAL" and "year" in doc[ent.end:min(ent.end+2, len(doc))].text.lower():
                try:
                    claim_data.policyholder_age = int(ent.text)
                    break
                except ValueError:
                    pass
        
        if not claim_data.policyholder_age:
            age_match = re.search(r'(\d+)[\s-]*year[\s-]*old', text, re.IGNORECASE)
            if age_match:
                claim_data.policyholder_age = int(age_match.group(1))
        
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"] and ent.text in ClaimExtractor.regions:
                claim_data.claim_region = ent.text
                break
        
        if not claim_data.claim_region:
            for region in ClaimExtractor.regions:
                if re.search(rf'\b{region}\b', text, re.IGNORECASE):
                    claim_data.claim_region = region
                    break
        
        for warranty in ClaimExtractor.warranty_types:
            if warranty.lower() in text.lower():
                claim_data.warranty = warranty
                break
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"] and ent.text in ClaimExtractor.brands:
                claim_data.vehicle_brand = ent.text
                break
        
        if not claim_data.vehicle_brand:
            for brand in ClaimExtractor.brands:
                if re.search(rf'\b{brand}\b', text, re.IGNORECASE):
                    claim_data.vehicle_brand = brand
                    break
        
        if claim_data.vehicle_brand:
            brand_models = ClaimExtractor.models.get(claim_data.vehicle_brand, [])
            for model in brand_models:
                if re.search(rf'\b{model}\b', text, re.IGNORECASE):
                    claim_data.vehicle_model = model
                    break
        
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                amount_str = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)', ent.text)
                if amount_str:
                    try:
                        amount_str = amount_str.group(1).replace(',', '')
                        claim_data.claim_amount_paid = float(amount_str)
                        
                        if any(currency in ent.text.lower() for currency in ['€', 'eur', 'euro']):
                            break
                    except ValueError:
                        pass
        
        if not claim_data.claim_amount_paid:
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
