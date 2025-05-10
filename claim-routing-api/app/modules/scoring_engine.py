from app.models.claim import ClaimData


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
            if claim_data.premium_amount_paid > 1500:
                customer_value = "VIP"
                reasons.append(f"Premium > €1,500 (€{claim_data.premium_amount_paid:.2f})")
            elif claim_data.premium_amount_paid > 1000:
                customer_value = "Premium"
                reasons.append(f"Premium > €1,000 (€{claim_data.premium_amount_paid:.2f})")
            else:
                customer_value = "Standard"
                reasons.append(f"Standard premium (€{claim_data.premium_amount_paid:.2f})")
        else:
            customer_value = "Standard"
            reasons.append("Premium amount unknown")
            
        return customer_value, reasons
