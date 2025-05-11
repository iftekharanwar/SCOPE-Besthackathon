import uuid
from app.models.claim import ClaimData, RoutingDecision, FraudIndicator
from app.modules.scoring_engine import ScoringEngine
from app.modules.ml_routing_engine import ml_routing_engine


class RoutingEngine:
    """Route claims to appropriate teams based on claim data and scores"""

    @staticmethod
    def route_claim(claim_data: ClaimData) -> RoutingDecision:
        """
        Determine the appropriate team for a claim based on its characteristics
        Uses a hybrid approach combining ML predictions and rule-based routing
        Returns a RoutingDecision with team assignment and reasoning
        """
        urgency_score, urgency_level, urgency_reasons = ScoringEngine.calculate_urgency(claim_data)
        risk_score, risk_reasons = ScoringEngine.calculate_risk(claim_data)
        customer_value, value_reasons = ScoringEngine.calculate_customer_value(claim_data)
        
        fraud_indicator = ScoringEngine.detect_fraud(claim_data)
        claim_data.fraud_indicator = fraud_indicator
        
        all_reasons = urgency_reasons + risk_reasons + value_reasons
        
        if fraud_indicator.is_potential_fraud:
            all_reasons.extend(fraud_indicator.fraud_indicators)
        
        ml_reasons = []
        if ml_routing_engine.is_model_available:
            claim_dict = {
                'policyholder_age': claim_data.policyholder_age,
                'policyholder_gender': claim_data.policyholder_gender,
                'warranty': claim_data.warranty,
                'claim_region': claim_data.claim_region,
                'claim_province': claim_data.claim_province,
                'vehicle_brand': claim_data.vehicle_brand,
                'vehicle_model': claim_data.vehicle_model,
                'claim_amount_paid': claim_data.claim_amount_paid,
                'premium_amount_paid': claim_data.premium_amount_paid,
                'claim_date': claim_data.claim_date
            }
            
            _, _, ml_reasons = ml_routing_engine.predict_department(claim_dict)
            
            if ml_reasons and ml_reasons[0] != "ML model not available":
                all_reasons.extend([f"ML: {reason}" for reason in ml_reasons])
        
        assigned_team = RoutingEngine._assign_team(
            claim_data, 
            urgency_level, 
            risk_score, 
            customer_value, 
            fraud_indicator
        )
        
        claim_id = claim_data.claim_id or f"CLAIM-{uuid.uuid4().hex[:8].upper()}"
        
        decision = RoutingDecision(
            assigned_team=assigned_team,
            urgency=urgency_level,
            risk_score=risk_score,
            customer_value=customer_value,
            reasoning=all_reasons,
            claim_data=claim_data,
            claim_id=claim_id,
            is_potential_fraud=fraud_indicator.is_potential_fraud,
            fraud_indicators=fraud_indicator.fraud_indicators
        )
        
        return decision
    
    @staticmethod
    def _assign_team(
        claim_data: ClaimData, 
        urgency: str, 
        risk_score: float, 
        customer_value: str,
        fraud_indicator: FraudIndicator
    ) -> str:
        """Assign claim to appropriate team based on ML predictions and business rules"""
        
        if fraud_indicator.is_potential_fraud:
            return "Fraud Investigation Team"
        
        if ml_routing_engine.is_model_available:
            claim_dict = {
                'policyholder_age': claim_data.policyholder_age,
                'policyholder_gender': claim_data.policyholder_gender,
                'warranty': claim_data.warranty,
                'claim_region': claim_data.claim_region,
                'claim_province': claim_data.claim_province,
                'vehicle_brand': claim_data.vehicle_brand,
                'vehicle_model': claim_data.vehicle_model,
                'claim_amount_paid': claim_data.claim_amount_paid,
                'premium_amount_paid': claim_data.premium_amount_paid,
                'claim_date': claim_data.claim_date
            }
            
            ml_department, confidence, ml_reasons = ml_routing_engine.predict_department(claim_dict)
            
            if ml_department and confidence > 0.7:
                if ml_department == "High Value Claims":
                    region = claim_data.claim_region or "Central"
                    return f"High Value Claims - {region}"
                elif ml_department == "Legal Claims":
                    return "Legal Claims Department"
                elif ml_department == "Senior Claims":
                    return "Senior High-Risk Claims"
                elif ml_department == "VIP Claims":
                    return "VIP Customer Service"
                elif ml_department == "Regional Team - South":
                    return "Regional Team - South"
                elif ml_department == "Standard Claims":
                    pass
        
        if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 15000:
            region = claim_data.claim_region or "Central"
            return f"High Value Claims - {region}"
        
        if claim_data.warranty and "third-party" in claim_data.warranty.lower():
            return "Legal Claims Department"
        
        if claim_data.policyholder_age and claim_data.policyholder_age > 60 and claim_data.claim_amount_paid and claim_data.claim_amount_paid > 10000:
            return "Senior High-Risk Claims"
        
        if customer_value == "VIP":
            return "VIP Customer Service"
        
        if claim_data.claim_region in ["Napoli", "Naples", "Caserta"]:
            return "Regional Team - South"
        
        if urgency == "High" and risk_score > 0.7:
            return "Urgent High-Risk Claims"
        elif urgency == "High":
            return "Urgent Claims Processing"
        elif risk_score > 0.7:
            return "High-Risk Claims Processing"
        else:
            return "Standard Claims Processing"
