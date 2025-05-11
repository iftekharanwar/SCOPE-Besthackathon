from app.models.claim import ClaimData, FraudIndicator


class ScoringEngine:
    """Calculate urgency, risk, and customer value scores for claims"""

    @staticmethod
    def calculate_urgency(claim_data: ClaimData) -> tuple:
        """
        Calculate urgency score and level
        Returns: (urgency_score, urgency_level, reasons)
        """
        score = 0.0
        reasons = []
        
        if claim_data.claim_amount_paid:
            if claim_data.claim_amount_paid > 15000:
                score += 0.4
                reasons.append(f"Claim amount > €15,000 (€{claim_data.claim_amount_paid:.2f})")
            elif claim_data.claim_amount_paid > 10000:
                score += 0.3
                reasons.append(f"Claim amount > €10,000 (€{claim_data.claim_amount_paid:.2f})")
            elif claim_data.claim_amount_paid > 5000:
                score += 0.2
                reasons.append(f"Claim amount > €5,000 (€{claim_data.claim_amount_paid:.2f})")
        
        if claim_data.policyholder_age:
            if claim_data.policyholder_age > 70:
                score += 0.3
                reasons.append(f"Policyholder age > 70 ({claim_data.policyholder_age})")
            elif claim_data.policyholder_age > 60:
                score += 0.2
                reasons.append(f"Policyholder age > 60 ({claim_data.policyholder_age})")
        
        if claim_data.warranty and "third-party" in claim_data.warranty.lower():
            score += 0.3
            reasons.append("Third-party liability claim")
        
        if score >= 0.6:
            urgency_level = "High"
        elif score >= 0.3:
            urgency_level = "Medium"
        else:
            urgency_level = "Low"
            
        return score, urgency_level, reasons

    @staticmethod
    def calculate_risk(claim_data: ClaimData) -> tuple:
        """
        Calculate risk score
        Returns: (risk_score, reasons)
        """
        score = 0.0
        reasons = []
        
        luxury_brands = ["BMW", "Mercedes", "Audi", "Ferrari", "Lamborghini", "Maserati"]
        if claim_data.vehicle_brand in luxury_brands:
            score += 0.3
            reasons.append(f"Luxury vehicle brand ({claim_data.vehicle_brand})")
        
        if claim_data.claim_amount_paid:
            if claim_data.claim_amount_paid > 20000:
                score += 0.4
                reasons.append(f"Very high claim amount (€{claim_data.claim_amount_paid:.2f})")
            elif claim_data.claim_amount_paid > 10000:
                score += 0.2
                reasons.append(f"High claim amount (€{claim_data.claim_amount_paid:.2f})")
        
        high_risk_regions = ["Napoli", "Naples", "Caserta"]
        if claim_data.claim_region in high_risk_regions:
            score += 0.3
            reasons.append(f"High-risk region ({claim_data.claim_region})")
        
        if claim_data.warranty and "third-party" in claim_data.warranty.lower():
            score += 0.2
            reasons.append("Third-party liability complexity")
            
        score = min(score, 1.0)
            
        return score, reasons

    @staticmethod
    def calculate_customer_value(claim_data: ClaimData) -> tuple:
        """
        Calculate customer value
        Returns: (customer_value_category, reasons)
        """
        reasons = []
        
        if claim_data.premium_amount_paid:
            if claim_data.premium_amount_paid > 800:
                customer_value = "VIP"
                reasons.append(f"Premium > €800 (€{claim_data.premium_amount_paid:.2f})")
            elif claim_data.premium_amount_paid > 500:
                customer_value = "Premium"
                reasons.append(f"Premium > €500 (€{claim_data.premium_amount_paid:.2f})")
            else:
                customer_value = "Standard"
                reasons.append(f"Standard premium (€{claim_data.premium_amount_paid:.2f})")
        else:
            if claim_data.vehicle_brand in ["Ferrari", "Lamborghini", "Maserati"]:
                customer_value = "VIP"
                reasons.append(f"Luxury vehicle brand ({claim_data.vehicle_brand})")
            elif claim_data.vehicle_brand in ["BMW", "Mercedes", "Audi"]:
                customer_value = "Premium"
                reasons.append(f"Premium vehicle brand ({claim_data.vehicle_brand})")
            else:
                customer_value = "Standard"
                reasons.append("Premium amount unknown")
            
        return customer_value, reasons
        
    @staticmethod
    def detect_fraud(claim_data: ClaimData) -> FraudIndicator:
        """
        Detect potential fraud indicators in a claim
        Returns: FraudIndicator with fraud score and reasons
        """
        fraud_indicator = FraudIndicator()
        fraud_score = 0.0
        fraud_indicators = []
        
        known_brands = ["BMW", "Mercedes", "Audi", "Volkswagen", "Toyota", "Honda", 
                       "Ford", "Fiat", "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo"]
        
        if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 25000:
            if not claim_data.vehicle_brand or claim_data.vehicle_brand not in known_brands:
                fraud_score += 0.5
                fraud_indicators.append(f"Very high claim amount (€{claim_data.claim_amount_paid:.2f}) with unknown vehicle brand")
        
        high_risk_regions = ["Napoli", "Naples", "Caserta"]
        if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 15000:
            if claim_data.claim_region in high_risk_regions:
                fraud_score += 0.4
                fraud_indicators.append(f"High claim amount in high-risk region ({claim_data.claim_region})")
        
        if claim_data.warranty and "third-party" in claim_data.warranty.lower():
            if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 20000:
                fraud_score += 0.3
                fraud_indicators.append("High third-party liability claim amount")
        
        missing_info_count = 0
        if not claim_data.policyholder_age:
            missing_info_count += 1
        if not claim_data.vehicle_brand:
            missing_info_count += 1
        if not claim_data.claim_region:
            missing_info_count += 1
            
        if missing_info_count >= 2 and claim_data.claim_amount_paid and claim_data.claim_amount_paid > 10000:
            fraud_score += 0.5
            fraud_indicators.append(f"Missing critical information ({missing_info_count} fields) with high claim amount")
        
        fraud_indicator.fraud_score = min(fraud_score, 1.0)
        fraud_indicator.fraud_indicators = fraud_indicators
        fraud_indicator.is_potential_fraud = fraud_score >= 0.5
        
        return fraud_indicator
